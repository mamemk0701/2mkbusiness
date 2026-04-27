from PIL import Image
import os

# Créer les dossiers
os.makedirs('/home/mame_m_kane/guindima_site/static/images/silicone', exist_ok=True)
os.makedirs('/home/mame_m_kane/guindima_site/static/images/nylon', exist_ok=True)

# === SILICONE ===
# Image: 5 colonnes x 3 lignes
img_silicone = Image.open('/home/mame_m_kane/guindima_site/static/images/silicon_watchs.png')
w, h = img_silicone.size

# Calculer les dimensions de chaque cellule
cols, rows = 5, 3
cell_w = w // cols
cell_h = h // rows

silicone_names = [
    # Ligne 1
    ['vert_nuage', 'rose_arc', 'noir_fleur', 'rouge_donut', 'vert_glace'],
    # Ligne 2
    ['rose_baleine', 'mauve_licorne', 'jaune_donut', 'vert_bonbon', 'rose_licorne'],
    # Ligne 3
    ['bleu_saturne', 'blanc_glace', 'bleu_dino', 'vert_dino', 'beige_licorne']
]

for row in range(rows):
    for col in range(cols):
        left = col * cell_w
        top = row * cell_h
        right = left + cell_w
        bottom = top + cell_h
        
        cropped = img_silicone.crop((left, top, right, bottom))
        name = silicone_names[row][col]
        cropped.save(f'/home/mame_m_kane/guindima_site/static/images/silicone/{name}.png')
        print(f'✅ Silicone: {name}.png')

# === NYLON ===
# Image: 4 colonnes x 2 lignes
img_nylon = Image.open('/home/mame_m_kane/guindima_site/static/images/Nylons_bracelet.png')
w, h = img_nylon.size

cols, rows = 4, 2
cell_w = w // cols
cell_h = h // rows

nylon_names = [
    # Ligne 1
    ['rouge', 'rainbow', 'sept_couleurs', 'jaune_vert'],
    # Ligne 2
    ['bleu', 'blanc', 'noir', 'rose_sable']
]

for row in range(rows):
    for col in range(cols):
        left = col * cell_w
        top = row * cell_h
        right = left + cell_w
        bottom = top + cell_h
        
        cropped = img_nylon.crop((left, top, right, bottom))
        name = nylon_names[row][col]
        cropped.save(f'/home/mame_m_kane/guindima_site/static/images/nylon/{name}.png')
        print(f'✅ Nylon: {name}.png')

print('\n🎉 Toutes les images ont été découpées !')
