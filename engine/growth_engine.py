import os
import sys
import json
import time
import random
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
LEADS_DIR = BASE_DIR / 'leads'
PAYLOADS_DIR = BASE_DIR / 'payloads'
os.makedirs(LEADS_DIR, exist_ok=True)
os.makedirs(PAYLOADS_DIR / 'prospects', exist_ok=True)
os.makedirs(PAYLOADS_DIR / 'outreach', exist_ok=True)
os.makedirs(PAYLOADS_DIR / 'audit_previews', exist_ok=True)

from auditor import generate_creator_audit
from outreach import generate_dm_pitch
from free_trial import dispatch_free_trial

QUEUE_FILE = LEADS_DIR / 'prospect_queue.json'
CONTACTED_FILE = LEADS_DIR / 'contacted_leads.json'

TARGET_TAGS = [
    "modeloscolombia",
    "modelosmexicanas",
    "creadorasdecontenido",
    "modeloslatinas",
    "ugclatina",
    "fitnesslatina"
]

def load_contacted():
    if CONTACTED_FILE.exists():
        try:
            with open(CONTACTED_FILE, 'r', encoding='utf-8') as f:
                return [x.get('handle', '').lower() for x in json.load(f)]
        except Exception:
            return []
    return []

def load_queue():
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_queue(queue):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

class AkbalGrowthEngine:
    def __init__(self, cdp_url='http://127.0.0.1:9223'):
        self.cdp_url = cdp_url

    async def run_prospecting_cycle(self, max_new=5):
        """Descubre y califica nuevas creadoras latinas desde Instagram."""
        contacted = load_contacted()
        queue = load_queue()
        queued_handles = [x.get('handle', '').lower() for x in queue]
        
        print("\n=======================================================")
        print("🔍 AKBAL GROWTH ENGINE // CICLO DE RASTREO Y CALIFICACIÓN")
        print("=======================================================\n")
        
        tag = random.choice(TARGET_TAGS)
        tag_url = f"https://www.instagram.com/explore/tags/{tag}/"
        print(f"[1/4] Explorando hashtag de alta densidad: #{tag}")
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.cdp_url)
            ctx = browser.contexts[0]
            page = ctx.pages[0]
            await page.bring_to_front()
            
            try:
                await page.goto(tag_url, timeout=25000)
                await page.wait_for_timeout(4000)
            except Exception as e:
                print(f"Error cargando tag: {e}")
                return []
                
            # Extract post links
            post_links = await page.evaluate('''() => {
                const anchors = Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]'));
                return anchors.map(a => a.href).filter(h => h);
            }''')
            
            unique_posts = list(dict.fromkeys(post_links))[:12]
            print(f"[2/4] Encontradas {len(unique_posts)} publicaciones candidatas.")
            
            new_qualified = []
            for post_url in unique_posts:
                if len(new_qualified) >= max_new:
                    break
                    
                print(f"\n  Inspeccionando: {post_url}")
                try:
                    await page.goto(post_url, timeout=20000)
                    await page.wait_for_timeout(3000)
                except Exception:
                    continue
                    
                author_handle = await page.evaluate('''() => {
                    const container = document.querySelector('article, [role="dialog"], main');
                    if (!container) return null;
                    const links = Array.from(container.querySelectorAll('a[href^="/"]'));
                    for (let a of links) {
                        const href = a.getAttribute('href') || '';
                        const clean = href.replace(/\\//g, '').trim();
                        if (!clean || ['p', 'reel', 'reels', 'explore', 'direct', 'stories', 'akbal_mgt'].includes(clean) || href.startsWith('/p/') || href.startsWith('/reel/')) {
                            continue;
                        }
                        return clean;
                    }
                    return null;
                }''')
                
                if not author_handle or author_handle.lower() in contacted or author_handle.lower() in queued_handles:
                    print(f"    ⏭️ Omitiendo autor ({author_handle}): ya contactado o en cola.")
                    continue
                    
                # Check author profile
                profile_url = f"https://www.instagram.com/{author_handle}/"
                print(f"    👉 Evaluando perfil: @{author_handle}")
                await page.goto(profile_url, timeout=20000)
                await page.wait_for_timeout(3500)
                
                profile_meta = await page.evaluate('''() => {
                    const title = document.title || '';
                    const nameEl = document.querySelector('header section h1') || document.querySelector('header h2') || document.querySelector('header span');
                    const name = nameEl ? nameEl.textContent.trim() : '';
                    
                    const listItems = Array.from(document.querySelectorAll('header section ul li'));
                    let followersText = listItems.length >= 2 ? listItems[1].textContent : '';
                    
                    const links = Array.from(document.querySelectorAll('header a[target="_blank"], header a[href*="http"]'));
                    const bioLinks = links.map(l => l.href || l.textContent);
                    
                    return { name, followersText, bioLinks };
                }''')
                
                followers_str = profile_meta.get('followersText', '')
                print(f"    📊 Seguidores: {followers_str} | Enlaces: {len(profile_meta.get('bioLinks', []))}")
                
                # Check sweet spot
                prospect_obj = {
                    "handle": author_handle,
                    "name": profile_meta.get('name') or author_handle,
                    "profile_url": profile_url,
                    "followers_raw": followers_str,
                    "bio_links": profile_meta.get('bioLinks', []),
                    "discovered_at": time.time()
                }
                new_qualified.append(prospect_obj)
                queue.append(prospect_obj)
                queued_handles.append(author_handle.lower())
                print(f"    ⭐ CREADORA CALIFICADA Y AGREGADA A LA COLA: @{author_handle}")
                
            save_queue(queue)
            print(f"\n[3/4] Cola total actualizada: {len(queue)} creadoras listas para contacto.")
            return new_qualified

    async def run_dispatch_cycle(self, count=2):
        """Despacha DMs a las siguientes creadoras en cola con la oferta de prueba gratis."""
        from send_outreach_dm import send_dm
        
        queue = load_queue()
        contacted = load_contacted()
        
        to_dispatch = [q for q in queue if q.get('handle', '').lower() not in contacted][:count]
        if not to_dispatch:
            print("\n[DISPATCH] No hay creadoras pendientes en cola. Ejecutando ciclo de rastreo...")
            await self.run_prospecting_cycle(max_new=4)
            queue = load_queue()
            to_dispatch = [q for q in queue if q.get('handle', '').lower() not in contacted][:count]
            
        print(f"\n=======================================================")
        print(f"⚡ AKBAL DISPATCH ENGINE // ENVIANDO {len(to_dispatch)} DMS CON PRUEBA GRATIS")
        print(f"=======================================================\n")
        
        for item in to_dispatch:
            handle = item.get('handle')
            name = item.get('name', handle)
            first_name = name.split()[0] if name else handle
            
            pitch = (
                f"Hola {first_name}, qué tal. Te escribimos desde la dirección de @akbal_mgt (57K).\n\n"
                f"Estuvimos viendo tu contenido y tiene calidad evidente de Top 1%, pero el algoritmo te tiene limitada a tráfico local, cuando los ingresos reales en plataformas privadas provienen de suscriptores en Estados Unidos y Europa.\n\n"
                f"Sabemos que en internet abundan las promesas vacías. Para que veas resultados reales antes de evaluar nada, te ofrecemos una prueba 100% gratuita en tu propia cuenta: mándanos el link de tu último Reel y en 15 minutos le inyectamos 200 likes y comentarios estratégicos en español.\n\n"
                f"Si te gusta cómo responde el algoritmo, evaluamos darte acceso a nuestros planes desde $49 USD/mes (100% de tus ingresos para ti). ¿Cuál es el link de tu Reel más reciente?"
            )
            
            success = await send_dm(handle, pitch)
            if success:
                print(f"  ✓ Contactada con éxito: @{handle}")
            # Pacing delay between DMs for safety
            await asyncio.sleep(random.uniform(15, 25))

if __name__ == '__main__':
    engine = AkbalGrowthEngine()
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    
    if mode == 'scout':
        asyncio.run(engine.run_prospecting_cycle(max_new=5))
    elif mode == 'dispatch':
        asyncio.run(engine.run_dispatch_cycle(count=2))
    elif mode == 'full':
        async def full_flow():
            await engine.run_prospecting_cycle(max_new=3)
            await engine.run_dispatch_cycle(count=2)
        asyncio.run(full_flow())
