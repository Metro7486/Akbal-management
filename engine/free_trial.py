import os
import sys
import argparse
from pathlib import Path

# Add engine to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from mtp_dispatcher import MTPDispatcher
from config import WHITELISTED_SERVICES

TRIAL_COMMENTS = [
    "Increíble este look, la iluminación quedó top! ✨",
    "De dónde es el outfit? Te queda hermoso 💖",
    "Simplemente a otro nivel... 🔥",
    "Diosa total! El contenido está genial 😍"
]

def dispatch_free_trial(post_url: str):
    """
    Despacha la Micro-Prueba de Autoridad Gratuita (Cero Riesgo).
    Entrega: 200 likes de alta retención + 2,000 views en Reels + 4 comentarios estratégicos.
    Costo total: ~$0.15 USD.
    """
    clean_url = post_url.strip()
    if not clean_url.startswith('http'):
        clean_url = f"https://www.instagram.com/p/{clean_url}/"
        
    print(f"\n=======================================================")
    print(f"🎁 DESPACHANDO MICRO-PRUEBA GRATIS DE AUTORIDAD (BBB)")
    print(f"URL Objetivo: {clean_url}")
    print(f"=======================================================\n")
    
    dispatcher = MTPDispatcher()
    
    # 1. Inyectar 200 likes reales
    print("[1/3] Inyectando 200 likes de alta retención...")
    like_res = dispatcher.add_order(
        service_id=WHITELISTED_SERVICES['IG_LIKES_REAL']['id'],
        link=clean_url,
        quantity=200
    )
    print(f"  ✓ Orden de likes creada: {like_res}")
    
    # 2. Inyectar 2,000 views de Reel si aplica
    print("[2/3] Inyectando 2,000 vistas de Reel...")
    views_res = dispatcher.add_order(
        service_id=WHITELISTED_SERVICES['IG_REEL_VIEWS']['id'],
        link=clean_url,
        quantity=2000
    )
    print(f"  ✓ Orden de views creada: {views_res}")
    
    # 3. Inyectar comentarios en español (servicio 9825 si está activo)
    print("[3/3] Inyectando comentarios estratégicos en español...")
    custom_comments_text = "\n".join(TRIAL_COMMENTS)
    comments_payload = {
        'action': 'add',
        'service': 9825,  # Instagram Custom Comments
        'link': clean_url,
        'comments': custom_comments_text
    }
    comments_res = dispatcher._post(comments_payload)
    print(f"  ✓ Orden de comentarios creada: {comments_res}")
    
    print("\n=======================================================")
    print("✅ MICRO-PRUEBA DESPACHADA EXITOSAMENTE")
    print("Costo para nosotros: ~$0.15 USD")
    print("Efecto en la creadora: Notificaciones inmediatas en su celular")
    print("=======================================================\n")
    return {
        "likes": like_res,
        "views": views_res,
        "comments": comments_res
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Despachador de Micro-Prueba Gratuita | Akbal Management')
    parser.add_argument('--url', required=True, help='Enlace al Reel o publicación de Instagram')
    args = parser.parse_args()
    dispatch_free_trial(args.url)
