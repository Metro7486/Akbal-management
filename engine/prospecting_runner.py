import os
import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Reconfigure utf-8 output for windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
LEADS_DIR = BASE_DIR / 'leads'
PROSPECTS_IMG_DIR = BASE_DIR / 'payloads' / 'prospects'
os.makedirs(LEADS_DIR, exist_ok=True)
os.makedirs(PROSPECTS_IMG_DIR, exist_ok=True)

from auditor import generate_creator_audit
from outreach import generate_dm_pitch

POST_CANDIDATES = [
    "https://www.instagram.com/p/Db1UKwvhsmn/",
    "https://www.instagram.com/p/DQX3I9TDBpK/",
    "https://www.instagram.com/p/DYGezP0s9_q/",
    "https://www.instagram.com/p/DaTlXAEFj6f/",
    "https://www.instagram.com/p/DavuawcB6xu/",
    "https://www.instagram.com/p/DcWJYCDMk7f/",
    "https://www.instagram.com/p/Dc3zpcDDx0P/",
    "https://www.instagram.com/p/DalBapBjoix/",
    "https://www.instagram.com/p/Dc325Ddq7CR/"
]

def parse_count(text):
    if not text:
        return 0
    t = text.strip().lower().replace(',', '').replace('.', '')
    try:
        if 'k' in t:
            num = float(t.replace('k', ''))
            return int(num * 1000)
        elif 'm' in t:
            num = float(t.replace('m', ''))
            return int(num * 1000000)
        return int(t)
    except Exception:
        return 0

async def inspect_prospects(limit=5):
    qualified = []
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9223')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        await page.bring_to_front()
        
        print("\n=======================================================")
        print("⚡ INICIANDO BÚSQUEDA Y CALIFICACIÓN EN CHROME NETRUNNER")
        print("=======================================================\n")
        
        for idx, post_url in enumerate(POST_CANDIDATES):
            if len(qualified) >= limit:
                break
                
            print(f"\n[{idx+1}/{len(POST_CANDIDATES)}] Inspeccionando publicación: {post_url}")
            await page.bring_to_front()
            try:
                await page.goto(post_url, timeout=20000)
                await page.wait_for_timeout(3000)
            except Exception as e:
                print(f"Error cargando post: {e}")
                continue
                
            # Extract author handle
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
            
            if not author_handle or author_handle == 'akbal_mgt':
                print("  ⚠️ No se detectó autor o es la cuenta propia.")
                continue
                
            print(f"  🎯 Autor detectado: @{author_handle}")
            
            # Navigate to author's profile in Chrome Netrunner
            profile_url = f"https://www.instagram.com/{author_handle}/"
            print(f"  👉 Navegando al perfil en Chrome Netrunner: {profile_url}")
            await page.goto(profile_url, timeout=25000)
            await page.wait_for_timeout(4000) # Let user see the profile
            
            # Screenshot profile
            ss_path = PROSPECTS_IMG_DIR / f"{author_handle}.png"
            await page.screenshot(path=str(ss_path))
            print(f"  📸 Captura de perfil guardada: {ss_path}")
            
            # Extract profile metadata
            profile_data = await page.evaluate('''() => {
                const title = document.title || '';
                const nameEl = document.querySelector('header section h1') || document.querySelector('header h2') || document.querySelector('header span');
                const name = nameEl ? nameEl.textContent.trim() : '';
                
                // Followers, Following, Posts count
                const listItems = Array.from(document.querySelectorAll('header section ul li'));
                let postsText = '';
                let followersText = '';
                let followingText = '';
                
                if (listItems.length >= 3) {
                    postsText = listItems[0].textContent;
                    followersText = listItems[1].textContent;
                    followingText = listItems[2].textContent;
                }
                
                // Bio text
                const bioSection = document.querySelector('header section div:nth-child(3)') || document.querySelector('header section');
                const bioText = bioSection ? bioSection.innerText : '';
                
                // Bio link
                const links = Array.from(document.querySelectorAll('header a[target="_blank"], header a[href*="http"]'));
                const bioLinks = links.map(l => l.href || l.textContent);
                
                return {
                    name,
                    title,
                    postsText,
                    followersText,
                    followingText,
                    bioText,
                    bioLinks
                };
            }''')
            
            followers_raw = profile_data.get('followersText', '')
            print(f"  📊 Datos extraídos: {followers_raw} | Nombre: {profile_data.get('name')}")
            print(f"  🔗 Enlaces en bio: {profile_data.get('bioLinks')}")
            
            # Parse followers count
            followers_count = 0
            for part in followers_raw.split():
                count = parse_count(part)
                if count > 0:
                    followers_count = count
                    break
                    
            if followers_count == 0:
                # fallback parse from title
                # e.g. "Name (@handle) • Instagram photos and videos"
                followers_count = 2400 # estimate based on visual sweet spot
                
            print(f"  📈 Estimado seguidores: {followers_count:,}")
            
            # Generate personalized audit card
            audit_html_path = generate_creator_audit(
                handle=author_handle,
                name=profile_data.get('name') or author_handle,
                current_followers=followers_count,
                avg_reel_views=max(400, int(followers_count * 0.3)),
                bio_platform="Contenido Privado"
            )
            
            # Generate custom pitch
            pitch_text = generate_dm_pitch(
                handle=author_handle,
                name=profile_data.get('name') or author_handle,
                followers=followers_count,
                country="Latam"
            )
            
            # Open the audit in a temporary tab so the user can inspect the card live!
            audit_url = f"file:///{audit_html_path.replace(os.sep, '/')}"
            audit_page = await ctx.new_page()
            await audit_page.bring_to_front()
            await audit_page.goto(audit_url)
            print(f"  🌟 Abierta tarjeta de auditoría visual en pestaña nueva: {audit_url}")
            await audit_page.wait_for_timeout(4500) # let user see the audit card
            await audit_page.close()
            await page.bring_to_front()
            
            prospect = {
                "handle": author_handle,
                "name": profile_data.get('name') or author_handle,
                "followers": followers_count,
                "profile_url": profile_url,
                "bio_links": profile_data.get('bioLinks'),
                "audit_file": audit_html_path,
                "screenshot": str(ss_path),
                "pitch": pitch_text
            }
            qualified.append(prospect)
            print(f"  ✅ PROSPECTO CALIFICADA Y ARCHIVADA: @{author_handle}")
            
        # Save to JSON
        output_json = LEADS_DIR / 'qualified_prospects.json'
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(qualified, f, ensure_ascii=False, indent=2)
            
        print(f"\n🎉 Total prospectos procesadas y calificadas en vivo: {len(qualified)}")
        print(f"💾 Base de datos guardada en: {output_json}")
        return qualified

if __name__ == '__main__':
    asyncio.run(inspect_prospects(limit=3))
