import os
import sys
import json
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
OUTREACH_IMG_DIR = BASE_DIR / 'payloads' / 'outreach'
os.makedirs(LEADS_DIR, exist_ok=True)
os.makedirs(OUTREACH_IMG_DIR, exist_ok=True)

CONTACTED_FILE = LEADS_DIR / 'contacted_leads.json'

async def send_dm(handle: str, message_text: str):
    clean_handle = handle.lstrip('@')
    print(f"\n=======================================================")
    print(f"🚀 ENVIANDO CONTACTO DIRECTO EN VIVO A: @{clean_handle}")
    print(f"=======================================================\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9223')
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        await page.bring_to_front()
        
        # 1. Navigate to target profile
        profile_url = f"https://www.instagram.com/{clean_handle}/"
        print(f"[1/5] Navegando al perfil: {profile_url}")
        await page.goto(profile_url, timeout=25000)
        await page.wait_for_timeout(3500)
        
        # 2. Click on "Mensaje" button
        print("[2/5] Buscando botón 'Mensaje' en el perfil...")
        msg_btn = None
        selectors = [
            'div[role="button"]:has-text("Mensaje")',
            'button:has-text("Mensaje")',
            '//div[text()="Mensaje"]',
            '//button[contains(., "Mensaje")]',
            'div:text-is("Mensaje")',
            'a[href*="/direct/t/"]'
        ]
        
        for sel in selectors:
            try:
                el = await page.wait_for_selector(sel, timeout=3000)
                if el and await el.is_visible():
                    msg_btn = el
                    print(f"  ✓ Botón detectado con selector: {sel}")
                    break
            except Exception:
                continue
                
        if not msg_btn:
            # Check if there is an action menu or direct link
            print("  ⚠️ No se encontró el botón directo de 'Mensaje'. Buscando alternativas...")
            # Take debug screenshot
            await page.screenshot(path=str(OUTREACH_IMG_DIR / f"debug_{clean_handle}.png"))
            return False
            
        print("  👉 Haciendo clic en 'Mensaje'...")
        await msg_btn.click()
        await page.wait_for_timeout(4500)
        
        # Handle "Ahora no" notification dialog if it appears
        try:
            not_now = await page.query_selector('//button[text()="Ahora no" or text()="Not Now"]')
            if not_now and await not_now.is_visible():
                await not_now.click()
                print("  ✓ Diálogo de notificaciones descartado ('Ahora no')")
                await page.wait_for_timeout(1500)
        except Exception:
            pass
            
        # 3. Locate chat input box
        print("[3/5] Localizando caja de texto del chat...")
        input_selectors = [
            'div[contenteditable="true"][role="textbox"]',
            'div[contenteditable="true"][aria-label*="Mensaje"]',
            'div[contenteditable="true"]',
            'textarea[placeholder*="Mensaje"]',
            'p[contenteditable="true"]'
        ]
        
        chat_box = None
        for sel in input_selectors:
            try:
                el = await page.wait_for_selector(sel, timeout=4000)
                if el and await el.is_visible():
                    chat_box = el
                    print(f"  ✓ Caja de chat detectada con selector: {sel}")
                    break
            except Exception:
                continue
                
        if not chat_box:
            print("  ❌ No se pudo enfocar la caja de texto del chat.")
            await page.screenshot(path=str(OUTREACH_IMG_DIR / f"error_chat_{clean_handle}.png"))
            return False
            
        # 4. Type the personalized pitch into the chat
        print("[4/5] Escribiendo mensaje personalizado en la conversación...")
        await chat_box.click()
        await page.wait_for_timeout(800)
        
        # Insert text using insertText to preserve multiline and avoid rapid typing blocks
        # We can split by paragraphs or insert text cleanly
        paragraphs = [p.strip() for p in message_text.strip().split('\n\n') if p.strip()]
        
        for i, para in enumerate(paragraphs):
            # Type paragraph
            await page.keyboard.insert_text(para)
            if i < len(paragraphs) - 1:
                # Shift+Enter for new line inside same message bubble
                await page.keyboard.down("Shift")
                await page.keyboard.press("Enter")
                await page.keyboard.press("Enter")
                await page.keyboard.up("Shift")
            await page.wait_for_timeout(400)
            
        print("  ✓ Mensaje redactado completamente en la caja de texto.")
        await page.wait_for_timeout(2000)
        
        # 5. Send message
        print("[5/5] Enviando mensaje...")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(4000)
        
        # Screenshot chat confirmation
        confirm_path = OUTREACH_IMG_DIR / f"sent_{clean_handle}.png"
        await page.screenshot(path=str(confirm_path))
        print(f"  📸 Captura del mensaje enviado guardada en: {confirm_path}")
        
        # Log to contacted_leads.json
        contacted = []
        if CONTACTED_FILE.exists():
            try:
                with open(CONTACTED_FILE, 'r', encoding='utf-8') as f:
                    contacted = json.load(f)
            except Exception:
                contacted = []
                
        record = {
            "handle": clean_handle,
            "timestamp": asyncio.get_event_loop().time(),
            "status": "sent",
            "proof_screenshot": str(confirm_path),
            "message": message_text
        }
        contacted.append(record)
        with open(CONTACTED_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacted, f, ensure_ascii=False, indent=2)
            
        print(f"  ✅ CONTACTO COMPLETADO Y REGISTRADO EXITOSAMENTE: @{clean_handle}\n")
        return True

if __name__ == '__main__':
    import argparse
    from outreach import generate_dm_pitch
    
    parser = argparse.ArgumentParser(description='Despachador de DMs Directos | Akbal Management')
    parser.add_argument('--handle', default='valeortega.22', help='Usuario de Instagram')
    parser.add_argument('--name', default='Vale', help='Nombre público de la creadora')
    parser.add_argument('--followers', type=int, default=7600, help='Seguidores aproximados')
    parser.add_argument('--country', default='Chile', help='País de la creadora')
    args = parser.parse_args()
    
    # Generate tailored pitch
    pitch = (
        f"Hola {args.name}, qué tal. Te escribimos desde la dirección de @akbal_mgt (57K).\n\n"
        f"Estuvimos viendo tu perfil y tu contenido fotográfico y de pasarela tiene un estándar estético altísimo. Sin embargo, notamos que tu cuenta tiene {args.followers:,} seguidores y el algoritmo te tiene limitada en la retención de Reels, cuando el tráfico de mayor valor para creadoras independientes proviene de audiencias internacionales en Estados Unidos y Europa.\n\n"
        f"Tenemos un protocolo de aceleración diseñado para modelos y creadoras latinas: posicionamos tu cuenta con autoridad digital y comentarios estratégicos para atraer suscriptores con alto poder adquisitivo, y tú conservas el 100% de tus ingresos (sin comisiones del 50%).\n\n"
        f"Te preparamos un diagnóstico visual de 2 minutos para destrabar tu alcance. ¿Te gustaría revisarlo por aquí o a tu correo?"
    )
    
    asyncio.run(send_dm(args.handle, pitch))
