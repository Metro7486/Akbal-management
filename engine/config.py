import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

MTP_API_KEY = os.getenv('MTP_API_KEY', '')
MTP_API_URL = os.getenv('MTP_API_URL', 'https://morethanpanel.com/api/v2')

# Catalogo blindado con IDs y tarifas de MoreThanPanel para Creadoras / Modelos
WHITELISTED_SERVICES = {
    'IG_FOLLOWERS_HQ': {
        'id': 9751,
        'name': 'Instagram Followers | Lifetime Guaranteed | Drip-Feed ON',
        'rate': 4.06,  # por 1000
        'min': 10,
        'max': 10000000,
        'refill': True,
        'dripfeed': True
    },
    'IG_LIKES_REAL': {
        'id': 2519,
        'name': 'Instagram Real Likes + Reach + Impressions | 30 Day Refill',
        'rate': 0.48,  # por 1000
        'min': 20,
        'max': 500000,
        'refill': True,
        'dripfeed': True
    },
    'IG_REEL_VIEWS': {
        'id': 2505,
        'name': 'Instagram Reel Views | Lifetime Guaranteed',
        'rate': 0.02,  # por 1000
        'min': 100,
        'max': 1000000,
        'refill': True,
        'dripfeed': True
    },
    'TIKTOK_VIEWS_REAL': {
        'id': 9742,
        'name': 'Tiktok Real Views | 30 Day Refill | Low Drop | Drip-Feed ON',
        'rate': 0.14,  # por 1000
        'min': 100,
        'max': 500000000,
        'refill': True,
        'dripfeed': True
    }
}

# Paquetes comerciales oficiales de Akbal Management (Modelo BBB: Bueno, Bonito, Barato)
CREATOR_PACKAGES = {
    'FREE_TRIAL': {
        'name': 'Micro-Prueba de Autoridad (24 Horas Gratis)',
        'price_usd': 0.0,
        'wholesale_est': 0.15,
        'likes': 200,
        'reel_views': 2000,
        'custom_comments': 4,
        'target_audience': 'Prospectos nuevos para eliminar desconfianza y cerrar al 100%'
    },
    'LATAM_STARTER_49': {
        'name': 'Plan Impulso Latam (Starter Antidesconfianza)',
        'price_usd': 49.00,
        'wholesale_est': 1.70,
        'monthly_posts': 10,
        'likes_per_post': 200,
        'views_per_post': 1500,
        'comments_per_post': 5,
        'target_audience': 'Creadoras con <5K seguidores o que prueban por primera vez (Margen: 96.5%)'
    },
    'LATAM_PRO_129': {
        'name': 'Plan Autoridad Pro (Bestseller / Escalamiento)',
        'price_usd': 129.00,
        'wholesale_est': 15.12,
        'followers_boost': 2000,
        'monthly_posts': 20,
        'likes_per_post': 500,
        'views_per_post': 5000,
        'comments_per_post': 12,
        'target_audience': 'Creadoras de 3K a 25K seguidores que quieren monetizar en USD/EUR (Margen: 88.3%)'
    },
    'LATAM_ELITE_297': {
        'name': 'Plan Élite Top 1% (Escala Millonaria)',
        'price_usd': 297.00,
        'wholesale_est': 41.30,
        'followers_boost': 5000,
        'monthly_posts': 30,
        'likes_per_post': 1000,
        'views_per_post': 15000,
        'comments_per_post': 25,
        'target_audience': 'Modelos e influencers que facturan >$1,000 USD y buscan dominio total (Margen: 86.1%)'
    }
}
