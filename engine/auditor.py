import os
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / 'payloads' / 'audit_previews'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_creator_audit(handle: str, name: str, current_followers: int,
                           avg_reel_views: int, bio_platform: str = "OnlyFans") -> str:
    """
    Genera una tarjeta de auditoría visual de alto impacto para creadoras de contenido aspirantes.
    Diseñada para ser enviada por Instagram DM o WhatsApp desde @akbal_mgt.
    """
    clean_handle = handle.lstrip('@')
    target_followers = max(10000, int(current_followers * 4.5)) if current_followers < 2500 else current_followers + 15000
    target_views = max(35000, avg_reel_views * 8)
    est_lost_revenue = "$650 - $1,800 USD" if current_followers < 3000 else "$1,500 - $3,500 USD"

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Auditoría de Autoridad Digital | Akbal Management — @{clean_handle}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0A0A0C;
      color: #EAEAEA;
    }}
    .font-serif-lux {{
      font-family: 'Cormorant Garamond', serif;
    }}
    .card-border {{
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .gold-gradient {{
      background: linear-gradient(135deg, #D4AF37 0%, #F3E5AB 50%, #AA771C 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
  </style>
</head>
<body class="p-4 md:p-8 flex items-center justify-center min-h-screen">
  <div class="max-w-md w-full bg-[#121216] card-border rounded-2xl p-7 shadow-2xl relative overflow-hidden">
    <!-- Header de Agencia -->
    <div class="flex justify-between items-center pb-5 border-b border-white/5">
      <div>
        <span class="font-serif-lux text-xl tracking-wider text-white font-semibold">AKBAL</span>
        <span class="text-[9px] uppercase tracking-widest text-zinc-400 block font-medium">TALENT & CREATOR MANAGEMENT</span>
      </div>
      <div class="text-right">
        <span class="inline-flex items-center gap-1.5 bg-white/5 px-2.5 py-1 rounded-full text-[10px] text-zinc-300 font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          @akbal_mgt (57K)
        </span>
      </div>
    </div>

    <!-- Perfil Auditado -->
    <div class="mt-6">
      <div class="flex items-center justify-between">
        <span class="text-[10px] tracking-widest uppercase text-zinc-400 font-semibold">DIAGNÓSTICO ALGORÍTMICO</span>
        <span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 font-medium">{bio_platform} Funnel</span>
      </div>
      <h1 class="text-2xl font-serif-lux font-medium text-white mt-1.5">{name}</h1>
      <p class="text-xs text-zinc-400">@{clean_handle}</p>
    </div>

    <!-- Metricas Comparativas -->
    <div class="mt-6 grid grid-cols-2 gap-3">
      <!-- Estado Actual -->
      <div class="bg-[#18181F] card-border rounded-xl p-4">
        <span class="text-[9px] uppercase tracking-wider text-zinc-400 font-medium">Estado Actual</span>
        <p class="text-xl font-bold text-zinc-200 mt-2">{current_followers:,}</p>
        <p class="text-[10px] text-zinc-400">Seguidores en IG</p>
        <div class="mt-3 pt-3 border-t border-white/5">
          <p class="text-xs text-zinc-400">~{avg_reel_views:,} views/reel</p>
          <p class="text-[10px] text-rose-400 mt-0.5">Retención: Crítica</p>
        </div>
      </div>

      <!-- Con Aceleracion Akbal -->
      <div class="bg-[#18181F] border border-amber-500/30 rounded-xl p-4 relative">
        <div class="absolute top-0 right-0 bg-gradient-to-l from-amber-400 to-amber-600 text-black text-[8px] font-bold uppercase px-2 py-0.5 rounded-bl">
          Objetivo 7 Días
        </div>
        <span class="text-[9px] uppercase tracking-wider text-amber-400 font-semibold">Estatus Élite</span>
        <p class="text-xl font-bold text-white mt-2">{target_followers:,}</p>
        <p class="text-[10px] text-zinc-400">Seguidores de Autoridad</p>
        <div class="mt-3 pt-3 border-t border-white/5">
          <p class="text-xs text-amber-300">~{target_views:,}+ views/reel</p>
          <p class="text-[10px] text-emerald-400 mt-0.5">Tráfico a Link: +340%</p>
        </div>
      </div>
    </div>

    <!-- Bottleneck Alert -->
    <div class="mt-5 p-4 bg-amber-500/[0.04] border border-amber-500/20 rounded-xl">
      <p class="text-xs text-zinc-300 leading-relaxed">
        <strong class="text-white">Fuga de Suscripciones Detectada:</strong> Tu contenido fotográfico y estético tiene potencial de Top 1%, pero la falta de volumen de interacción en Instagram frena el algoritmo e impide que los suscriptores confíen en pagar una membresía premium.
      </p>
      <p class="text-[11px] text-amber-400/90 mt-2 font-medium">
        Pérdida estimada mensual en suscriptores: {est_lost_revenue}
      </p>
    </div>

    <!-- Call to Action -->
    <div class="mt-6 pt-4 border-t border-white/5 flex items-center justify-between">
      <div>
        <p class="text-[9px] uppercase text-zinc-400 tracking-wider">Protocolo Sugerido</p>
        <p class="text-xs font-semibold text-white">Tier 1: Creator Ignition</p>
      </div>
      <a href="https://instagram.com/akbal_mgt" target="_blank"
         class="bg-white hover:bg-zinc-200 text-black text-xs font-semibold px-4 py-2.5 rounded-lg transition-all">
        Contactar Dirección
      </a>
    </div>
  </div>
</body>
</html>'''

    output_file = OUTPUT_DIR / f'auditoria_{clean_handle}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[AUDITOR] Micro-auditoría generada exitosamente en: {output_file}")
    return str(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generador de Micro-Auditorías para Creadoras | Akbal Management')
    parser.add_argument('--handle', required=True, help='Usuario de Instagram (ej: sofia_glam)')
    parser.add_argument('--name', default='Creadora de Contenido', help='Nombre público del perfil')
    parser.add_argument('--followers', type=int, default=850, help='Número actual de seguidores')
    parser.add_argument('--views', type=int, default=300, help='Promedio actual de vistas por Reel')
    parser.add_argument('--platform', default='OnlyFans', help='Plataforma monetizada (OnlyFans, Fansly, etc.)')

    args = parser.parse_args()
    generate_creator_audit(args.handle, args.name, args.followers, args.views, args.platform)
