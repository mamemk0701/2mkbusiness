import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

# Produits et prix (mis à jour avril 2026)
PRODUCTS = {
    'T': {'name': 'Tracker GPS', 'price': 9000},
    'BN': {'name': 'Bracelet Nylon', 'price': 3500},
    'BS': {'name': 'Bracelet Silicone', 'price': 2500},
    'KS': {'name': 'Kit Saytu (Tracker + Silicone)', 'price': 11500},
    'KG': {'name': 'Kit Guëstu (Tracker + Nylon)', 'price': 12500},
}

# Couleurs Nylon (8 couleurs)
NYLON_COLORS = {
    'nr': 'Noir',
    'rg': 'Rouge',
    'rb': 'Rainbow',
    '7c': 'Sept couleurs',
    'jv': 'Jaune-Vert',
    'bl': 'Bleu',
    'bc': 'Blanc',
    'rs': 'Rose sable',
}

# Motifs Silicone (15 motifs - noms mis à jour)
SILICONE_DESIGNS = {
    'nua': 'Vert Nuage',
    'arc': 'Rose Arc-en-ciel',
    'fle': 'Noir Fleur',
    'don': 'Rouge Donut',
    'gla': 'Vert Menthe Glace',
    'bal': 'Rose Baleine',
    'lic': 'Mauve Licorne',
    'jdo': 'Jaune Donut',
    'bon': 'Vert Bonbon',
    'rli': 'Rose Licorne',
    'sat': 'Bleu Saturne',
    'bgl': 'Blanc Glace',
    'bdi': 'Bleu Dino',
    'vdi': 'Vert Dino',
    'bei': 'Beige Licorne',
}

ACOMPTE = 2000
