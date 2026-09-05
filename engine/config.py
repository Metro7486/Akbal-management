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

# Paquetes comerciales oficiales de Akbal Management para Creadoras OnlyFans / Modelos
CREATOR_PACKAGES = {
    'TIER_1_IGNITION': {
        'name': 'Creator Ignition (Social Proof Launch)',
        'price_usd': 190.00,
        'wholesale_est': 7.50,
        'followers': 5000,
        'reel_views': 50000,
        'likes': 1500,
        'target_audience': 'Aspirantes que recién abren OnlyFans o tienen <2K seguidores'
    },
    'TIER_2_PUSH': {
        'name': 'Algorithmic Push (Top 10% Surge)',
        'price_usd': 450.00,
        'wholesale_est': 18.00,
        'followers': 15000,
        'reel_views': 150000,
        'likes': 4000,
        'target_audience': 'Creadoras activas con tráfico estancado en reels'
    },
    'TIER_3_ELITE': {
        'name': 'Elite Talent Acceleration',
        'price_usd': 950.00,
        'wholesale_est': 42.00,
        'followers': 35000,
        'reel_views': 400000,
        'likes': 10000,
        'target_audience': 'Modelos y creadoras buscando estatus Top 1% y alianzas de agencia'
    }
}
