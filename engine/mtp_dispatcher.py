import os
import time
import json
import random
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter

try:
    from config import MTP_API_KEY, MTP_API_URL, WHITELISTED_SERVICES, CREATOR_PACKAGES, BASE_DIR
except ImportError:
    from engine.config import MTP_API_KEY, MTP_API_URL, WHITELISTED_SERVICES, CREATOR_PACKAGES, BASE_DIR

ORDERS_LOG_PATH = BASE_DIR / 'leads' / 'orders.json'

class MTPDispatcher:
    """Motor de despacho y arbitraje de infraestructura con MoreThanPanel para Akbal Management."""
    def __init__(self, base_url: str = MTP_API_URL, api_key: str = MTP_API_KEY, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=20, pool_maxsize=50)
        self.session.mount('https://', adapter)

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload['key'] = self.api_key
        backoff = 2.0
        for attempt in range(4):
            try:
                response = self.session.post(self.base_url, data=payload, timeout=self.timeout)
                if response.status_code == 429 or response.status_code in (502, 503, 504):
                    jitter = random.uniform(0.5, 1.5)
                    sleep_time = backoff + jitter
                    print(f'[WARN] HTTP {response.status_code}. Reintentando en {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
                    backoff *= 2
                    continue
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as ex:
                if attempt == 3:
                    return {'error': f'DISPATCHER_FAILED: {str(ex)}'}
                time.sleep(backoff)
                backoff *= 2
        return {'error': 'MAX_RETRIES_EXCEEDED'}

    def get_balance(self) -> Dict[str, Any]:
        """Obtiene el saldo disponible en la cuenta mayorista."""
        return self._post({'action': 'balance'})

    def add_order(self, service_id: int, link: str, quantity: int,
                  runs: Optional[int] = None, interval: Optional[int] = None) -> Dict[str, Any]:
        """Agrega una orden unitaria o con drip-feed."""
        data = {
            'action': 'add',
            'service': service_id,
            'link': link,
            'quantity': quantity
        }
        if runs and interval:
            data['runs'] = runs
            data['interval'] = interval
            print(f'[AKBAL-MTP] Drip-feed: {quantity}/lote x {runs} ejecuciones cada {interval}m (Total: {quantity * runs})')
        else:
            print(f'[AKBAL-MTP] Despacho Directo: {quantity} unidades al enlace: {link}')

        res = self._post(data)
        self._log_order(res, service_id, link, quantity, runs, interval)
        return res

    def get_batch_status(self, order_ids: List[int]) -> Dict[str, Any]:
        """Consulta el estado de hasta 100 órdenes de forma masiva."""
        if not order_ids:
            return {}
        if len(order_ids) > 100:
            raise ValueError('MTP API limita las consultas por lotes a máximo 100 IDs.')
        return self._post({
            'action': 'status',
            'orders': ','.join(map(str, order_ids))
        })

    def trigger_refill(self, order_id: int) -> Dict[str, Any]:
        """Dispara reposición garantizada si hubo caída de seguidores."""
        return self._post({
            'action': 'refill',
            'order': order_id
        })

    def dispatch_creator_package(self, package_key: str, profile_url: str,
                                 reel_urls: List[str]) -> Dict[str, Any]:
        """Despacha un paquete completo para una creadora con fraccionamiento seguro."""
        pkg = CREATOR_PACKAGES.get(package_key)
        if not pkg:
            raise ValueError(f'Paquete no reconocido: {package_key}')

        print(f"\n=======================================================")
        print(f"AKBAL MANAGEMENT // DESPACHANDO PAQUETE: {pkg['name']}")
        print(f"CLIENTE / PERFIL: {profile_url}")
        print(f"=======================================================")

        results = {'package': pkg['name'], 'orders': []}

        # 1. Despacho de seguidores con Drip-Feed (para parecer 100% orgánico)
        total_followers = pkg['followers']
        runs = 5 if total_followers <= 5000 else 10
        qty_per_run = total_followers // runs
        print(f"[1/3] Programando {total_followers} seguidores ({qty_per_run} c/90min en {runs} lotes)...")
        f_order = self.add_order(
            service_id=WHITELISTED_SERVICES['IG_FOLLOWERS_HQ']['id'],
            link=profile_url,
            quantity=qty_per_run,
            runs=runs,
            interval=90
        )
        results['orders'].append({'type': 'followers', 'response': f_order})

        # 2. Despacho de vistas en Reels
        if reel_urls:
            views_per_reel = pkg['reel_views'] // len(reel_urls)
            print(f"[2/3] Distribuyendo {pkg['reel_views']} vistas en {len(reel_urls)} Reels ({views_per_reel} c/u)...")
            for r_url in reel_urls:
                v_order = self.add_order(
                    service_id=WHITELISTED_SERVICES['IG_REEL_VIEWS']['id'],
                    link=r_url,
                    quantity=views_per_reel
                )
                results['orders'].append({'type': 'reel_views', 'link': r_url, 'response': v_order})
                time.sleep(1)

            # 3. Despacho de Likes en Reels
            likes_per_reel = pkg['likes'] // len(reel_urls)
            print(f"[3/3] Distribuyendo {pkg['likes']} likes en {len(reel_urls)} Reels ({likes_per_reel} c/u)...")
            for r_url in reel_urls:
                l_order = self.add_order(
                    service_id=WHITELISTED_SERVICES['IG_LIKES_REAL']['id'],
                    link=r_url,
                    quantity=likes_per_reel
                )
                results['orders'].append({'type': 'reel_likes', 'link': r_url, 'response': l_order})
                time.sleep(1)
        else:
            print("[AVISO] No se proporcionaron URLs de reels; se omite distribución de vistas y likes.")

        print(f"\n[ÉXITO] Paquete {pkg['name']} despachado correctamente.")
        return results

    def _log_order(self, response: Dict[str, Any], service_id: int, link: str,
                   quantity: int, runs: Optional[int], interval: Optional[int]):
        order_id = response.get('order')
        if not order_id:
            return

        os.makedirs(ORDERS_LOG_PATH.parent, exist_ok=True)
        orders = []
        if ORDERS_LOG_PATH.exists():
            try:
                with open(ORDERS_LOG_PATH, 'r', encoding='utf-8') as f:
                    orders = json.load(f)
            except Exception:
                orders = []

        record = {
            'order_id': order_id,
            'agency': 'Akbal Management',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'service_id': service_id,
            'link': link,
            'quantity_per_run': quantity,
            'runs': runs or 1,
            'interval_min': interval or 0,
            'total_units': (quantity * runs) if runs else quantity,
            'raw_response': response
        }
        orders.append(record)

        with open(ORDERS_LOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        print(f'[LOG] Orden #{order_id} registrada localmente en {ORDERS_LOG_PATH}')

def main():
    parser = argparse.ArgumentParser(description='Akbal Management - MTP Dispatcher Engine')
    parser.add_argument('--balance', action='store_true', help='Consultar saldo mayorista en MTP')
    parser.add_argument('--status', type=int, help='Consultar estado de una orden por ID')
    parser.add_argument('--batch-status', type=str, help='Consultar estados de órdenes separadas por coma')
    parser.add_argument('--refill', type=int, help='Disparar refill para una orden')
    parser.add_argument('--dispatch-pkg', choices=['TIER_1_IGNITION', 'TIER_2_PUSH', 'TIER_3_ELITE'],
                        help='Despachar paquete comercial completo para creadora')
    parser.add_argument('--profile', type=str, help='URL del perfil de Instagram')
    parser.add_argument('--reels', nargs='*', help='URLs de los reels para distribuir vistas y likes')
    parser.add_argument('--quick-followers', nargs=2, metavar=('PROFILE_URL', 'QTY'),
                        help='Despachar seguidores con Drip-Feed seguro')

    args = parser.parse_args()
    dispatcher = MTPDispatcher()

    if args.balance:
        bal = dispatcher.get_balance()
        print(f"[BALANCE MTP] Saldo disponible: {bal.get('balance')} {bal.get('currency')}")
    elif args.status:
        st = dispatcher.get_batch_status([args.status])
        print(json.dumps(st, indent=2))
    elif args.batch_status:
        ids = [int(x.strip()) for x in args.batch_status.split(',') if x.strip()]
        st = dispatcher.get_batch_status(ids)
        print(json.dumps(st, indent=2))
    elif args.refill:
        rf = dispatcher.trigger_refill(args.refill)
        print(json.dumps(rf, indent=2))
    elif args.dispatch_pkg:
        if not args.profile:
            print("[ERROR] Debe especificar --profile <URL>")
            return
        reels = args.reels or []
        res = dispatcher.dispatch_creator_package(args.dispatch_pkg, args.profile, reels)
        print(json.dumps(res, indent=2))
    elif args.quick_followers:
        link, qty_str = args.quick_followers
        qty = int(qty_str)
        runs = 5
        per_run = max(10, qty // runs)
        res = dispatcher.add_order(
            service_id=WHITELISTED_SERVICES['IG_FOLLOWERS_HQ']['id'],
            link=link,
            quantity=per_run,
            runs=runs,
            interval=90
        )
        print(f'[RESULTADO] {res}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
