import re
import requests
from config import Config, PRODUCTS, NYLON_COLORS, SILICONE_DESIGNS, ACOMPTE
from models import (
    get_or_create_client, create_order, get_order, get_pending_orders,
    get_today_orders, search_orders_by_phone, update_order_acompte,
    update_order_paid, update_order_shipping, update_order_delivered, get_stats,
    delete_order, update_client_info, cancel_order,
    get_all_stock, get_low_stock, update_stock, check_stock_availability, 
    deduct_stock_for_order, restore_stock_for_order, get_stock_item
)

TELEGRAM_API = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}"

# === TELEGRAM FUNCTIONS ===

def send_message(chat_id, text, parse_mode='HTML'):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    requests.post(url, data=data)

def set_webhook(webhook_url):
    url = f"{TELEGRAM_API}/setWebhook"
    data = {'url': webhook_url}
    response = requests.post(url, data=data)
    return response.json()

# === PARSING FUNCTIONS ===

def parse_order_command(text):
    """Parse: /cmd Nom, Phone, Adresse, Produits"""
    try:
        text = text.replace('/cmd ', '').strip()
        parts = [p.strip() for p in text.split(',', 3)]
        if len(parts) < 4:
            return None, "Format invalide. Utilise: /cmd Nom, Téléphone, Adresse, Produits"
        
        name, phone, address, products_str = parts
        phone = re.sub(r'[^\d]', '', phone)
        if len(phone) < 9:
            return None, "Numéro de téléphone invalide"
        
        items = []
        total = 0
        
        product_parts = products_str.split()
        for part in product_parts:
            match = re.match(r'([A-Z]+):(\d+)(?::(.+))?', part, re.IGNORECASE)
            if not match:
                return None, f"Format produit invalide: {part}"
            
            code = match.group(1).upper()
            qty = int(match.group(2))
            variants = match.group(3)
            
            if code not in PRODUCTS:
                return None, f"Produit inconnu: {code}"
            
            product = PRODUCTS[code]
            
            if variants:
                variant_list = [v.strip() for v in variants.split(',')]
                if len(variant_list) == 1:
                    variant_list = variant_list * qty
                elif len(variant_list) != qty:
                    return None, f"Nombre de variantes ({len(variant_list)}) != quantité ({qty}) pour {code}"
                
                for variant in variant_list:
                    variant_lower = variant.lower()
                    variant_name = None
                    variant_code = variant_lower
                    
                    if code in ['KG', 'BN']:
                        if variant_lower in NYLON_COLORS:
                            variant_name = NYLON_COLORS[variant_lower]
                        else:
                            return None, f"Couleur Nylon inconnue: {variant}"
                    elif code in ['KS', 'BS']:
                        if variant_lower in SILICONE_DESIGNS:
                            variant_name = SILICONE_DESIGNS[variant_lower]
                        else:
                            return None, f"Motif Silicone inconnu: {variant}"
                    
                    items.append({
                        'code': code,
                        'name': product['name'],
                        'variant': variant_name,
                        'variant_code': variant_code,
                        'quantity': 1,
                        'unit_price': product['price'],
                        'subtotal': product['price']
                    })
                    total += product['price']
            else:
                if code in ['KG', 'BN', 'KS', 'BS']:
                    return None, f"Couleur/motif requis pour {code}"
                
                items.append({
                    'code': code,
                    'name': product['name'],
                    'variant': None,
                    'variant_code': None,
                    'quantity': qty,
                    'unit_price': product['price'],
                    'subtotal': product['price'] * qty
                })
                total += product['price'] * qty
        
        return {
            'name': name,
            'phone': phone,
            'address': address,
            'items': items,
            'total': total
        }, None
        
    except Exception as e:
        return None, f"Erreur de parsing: {str(e)}"

# === FORMAT FUNCTIONS ===

def format_payment_status(status):
    statuses = {
        'pending': '⏳ En attente',
        'acompte': f'🔸 Acompte ({ACOMPTE:,} F)',
        'paid': '✅ Payé'
    }
    return statuses.get(status, status)

def format_delivery_status(status):
    statuses = {
        'preparation': '📦 En préparation',
        'shipping': '🚚 En cours',
        'delivered': '✅ Livré',
        'cancelled': '🚫 Annulée'
    }
    return statuses.get(status, status)

def format_order(order):
    items_text = ""
    for item in order.get('items', []):
        variant = f" ({item['variant']})" if item.get('variant') else ""
        if item['quantity'] > 1:
            items_text += f"  • {item['quantity']}x {item['product_name']}{variant} — {item['subtotal']:,} F\n"
        else:
            items_text += f"  • {item['product_name']}{variant} — {item['subtotal']:,} F\n"
    
    reste = order['total'] - order['acompte']
    reste_text = f"\n💵 Reste à payer : {reste:,} F" if reste > 0 and order['payment_status'] != 'pending' else ""
    
    return f"""📦 <b>Commande #{order['id']:03d}</b>

👤 {order['client_name'] or 'N/A'}
📞 {order['client_phone']}
📍 {order['client_address'] or 'N/A'}

🛒 Articles :
{items_text}
💰 Total : {order['total']:,} F{reste_text}

💳 Paiement : {format_payment_status(order['payment_status'])}
🚚 Livraison : {format_delivery_status(order['delivery_status'])}

📅 {order['created_at'].strftime('%d/%m/%Y %H:%M')}"""

def format_order_short(order):
    return f"#{order['id']:03d} | {order['client_name'] or order['client_phone']} | {order['total']:,} F | {format_payment_status(order['payment_status'])} | {format_delivery_status(order['delivery_status'])}"

# === COMMAND HANDLERS ===

def handle_start(chat_id):
    text = """👋 <b>Bienvenue sur MK Business Bot !</b>

🎯 Bot de gestion des commandes Guindima.

Tape /aide pour voir toutes les commandes disponibles."""
    send_message(chat_id, text)

def handle_aide(chat_id):
    text = """📋 <b>GUIDE RAPIDE GUINDIMA</b>

💰 <b>PRODUITS & PRIX :</b>
<code>T</code> = Tracker seul (13 000 F)
<code>BN</code> = Bracelet Nylon (5 000 F)
<code>BS</code> = Bracelet Silicone (4 000 F)
<code>KS</code> = Kit Saytu - Tracker+Silicone (17 000 F)
<code>KG</code> = Kit Guëstu - Tracker+Nylon (18 000 F)

🎨 <b>COULEURS NYLON</b> (pour KG et BN) :
<code>nr</code>=Noir | <code>rg</code>=Rouge | <code>rb</code>=Rainbow | <code>7c</code>=Sept couleurs
<code>jv</code>=Jaune-Vert | <code>bl</code>=Bleu | <code>bc</code>=Blanc | <code>rs</code>=Rose sable

🦄 <b>MOTIFS SILICONE</b> (pour KS et BS) :
<code>lic1</code>=Licorne café | <code>lic2</code>=Licorne tête | <code>lic3</code>=Licorne ailée
<code>gla</code>=Glace | <code>don1</code>=Donut licorne | <code>don2</code>=Donut noeud
<code>bal</code>=Baleine | <code>suc</code>=Sucettes | <code>cup</code>=Cupcake
<code>din1</code>=Dino fraise | <code>din2</code>=Dino bébé | <code>nua</code>=Nuage
<code>arc</code>=Arc-en-ciel | <code>sat</code>=Saturne | <code>fle</code>=Fleur

📝 <b>COMMANDES :</b>
/cmd Nom, Tél, Adresse, Produits → Nouvelle commande
/list → Commandes en attente
/today → Commandes du jour
/find 77123 → Chercher par téléphone
/stats → Statistiques
#47 → Voir commande #47

💳 <b>PAIEMENT :</b>
/acompte 47 → Acompte reçu (2 000 F)
/pay 47 → Paiement complet

🚚 <b>LIVRAISON :</b>
/ship 47 → En livraison
/done 47 → Livrée

✏️ <b>MODIFICATION :</b>
/edit 47 nom Aminata Fall → Modifier nom
/edit 47 tel 781234567 → Modifier téléphone
/edit 47 adr Plateau → Modifier adresse
/del 47 → Supprimer commande
/cancel 47 → Annuler commande

📦 <b>STOCK :</b>
/stock → Voir tout le stock
/lowstock → Produits en rupture/faible
/s+ T 10 → Ajouter 10 trackers
/s+ BN:nr 5 → Ajouter 5 bracelets Nylon Noir
/s- BS:bal 2 → Retirer 2 bracelets Silicone Baleine
/s= T 20 → Définir stock trackers à 20

📌 <b>EXEMPLES :</b>
<code>/cmd Fatou, 771234567, Almadies, KS:1:bal</code>
<code>/cmd Ibou, 781112233, Medina, KG:2:nr,rb T:1</code>"""
    send_message(chat_id, text)

def handle_cmd(chat_id, text):
    order_data, error = parse_order_command(text)
    
    if error:
        send_message(chat_id, f"❌ {error}")
        return
    
    # Vérifier le stock
    is_available, problems = check_stock_availability(order_data['items'])
    
    if not is_available:
        problems_text = "\n".join([f"  • {p}" for p in problems])
        send_message(chat_id, f"❌ <b>Stock insuffisant :</b>\n{problems_text}")
        return
    
    client = get_or_create_client(order_data['phone'], order_data['name'], order_data['address'])
    order = create_order(client['id'], order_data['items'], order_data['total'])
    
    # Déduire le stock
    deduct_stock_for_order(order_data['items'])
    
    full_order = get_order(order['id'])
    
    # Vérifier si stock faible après la commande
    low_stock = get_low_stock()
    low_stock_alert = ""
    if low_stock:
        low_items = [f"{s['variant_name'] or 'Tracker'} ({s['quantity']})" for s in low_stock[:3]]
        low_stock_alert = f"\n\n⚠️ <b>Stock faible :</b> {', '.join(low_items)}"
    
    send_message(chat_id, f"✅ Commande créée !\n\n{format_order(full_order)}{low_stock_alert}")

def handle_list(chat_id):
    orders = get_pending_orders()
    
    if not orders:
        send_message(chat_id, "📭 Aucune commande en attente.")
        return
    
    text = f"📋 <b>Commandes en attente ({len(orders)})</b>\n\n"
    for order in orders[:20]:
        text += f"{format_order_short(order)}\n"
    
    if len(orders) > 20:
        text += f"\n... et {len(orders) - 20} autres"
    
    send_message(chat_id, text)

def handle_today(chat_id):
    orders = get_today_orders()
    
    if not orders:
        send_message(chat_id, "📭 Aucune commande aujourd'hui.")
        return
    
    text = f"📅 <b>Commandes du jour ({len(orders)})</b>\n\n"
    for order in orders:
        text += f"{format_order_short(order)}\n"
    
    send_message(chat_id, text)

def handle_find(chat_id, phone):
    orders = search_orders_by_phone(phone)
    
    if not orders:
        send_message(chat_id, f"🔍 Aucune commande trouvée pour '{phone}'")
        return
    
    text = f"🔍 <b>Résultats pour '{phone}' ({len(orders)})</b>\n\n"
    for order in orders[:10]:
        text += f"{format_order_short(order)}\n"
    
    send_message(chat_id, text)

def handle_stats(chat_id):
    stats = get_stats()
    
    text = f"""📊 <b>STATISTIQUES</b>

📦 Total commandes : {stats['total_orders']}
💰 Revenus total : {stats['total_revenue']:,} F

📅 Aujourd'hui :
  • Commandes : {stats['today_orders']}
  • Revenus : {stats['today_revenue']:,} F

⏳ En attente : {stats['pending_orders']} commandes"""
    
    send_message(chat_id, text)

def handle_acompte(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = update_order_acompte(order_id)
        if order:
            full_order = get_order(order_id)
            send_message(chat_id, f"✅ Acompte enregistré !\n\n{format_order(full_order)}")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_pay(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = update_order_paid(order_id)
        if order:
            full_order = get_order(order_id)
            send_message(chat_id, f"✅ Paiement complet enregistré !\n\n{format_order(full_order)}")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_ship(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = update_order_shipping(order_id)
        if order:
            full_order = get_order(order_id)
            send_message(chat_id, f"🚚 Commande en livraison !\n\n{format_order(full_order)}")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_done(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = update_order_delivered(order_id)
        if order:
            full_order = get_order(order_id)
            send_message(chat_id, f"✅ Commande livrée !\n\n{format_order(full_order)}")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_show(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = get_order(order_id)
        if order:
            send_message(chat_id, format_order(order))
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_del(chat_id, order_id):
    try:
        order_id = int(order_id)
        order = get_order(order_id)
        if not order:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
            return
        
        # Restaurer le stock avant suppression
        restore_stock_for_order(order_id)
        
        if delete_order(order_id):
            send_message(chat_id, f"🗑️ Commande #{order_id:03d} supprimée (stock restauré)\n\n👤 {order['client_name']}\n💰 {order['total']:,} F")
        else:
            send_message(chat_id, f"❌ Erreur lors de la suppression")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_edit(chat_id, args):
    try:
        parts = args.split(' ', 2)
        if len(parts) < 3:
            send_message(chat_id, "❌ Format: /edit ID champ valeur\nChamps: nom, tel, adr")
            return
        
        order_id = int(parts[0])
        field = parts[1].lower()
        value = parts[2]
        
        field_map = {
            'nom': 'name', 'name': 'name',
            'tel': 'phone', 'phone': 'phone',
            'adr': 'address', 'adresse': 'address', 'address': 'address'
        }
        
        if field not in field_map:
            send_message(chat_id, "❌ Champ invalide. Utilise: nom, tel, adr")
            return
        
        if update_client_info(order_id, field_map[field], value):
            order = get_order(order_id)
            send_message(chat_id, f"✅ Commande #{order_id:03d} modifiée\n\n{format_order(order)}")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

def handle_cancel(chat_id, order_id):
    try:
        order_id = int(order_id)
        
        # Restaurer le stock avant annulation
        restore_stock_for_order(order_id)
        
        order = cancel_order(order_id)
        if order:
            send_message(chat_id, f"🚫 Commande #{order_id:03d} annulée (stock restauré)")
        else:
            send_message(chat_id, f"❌ Commande #{order_id} introuvable")
    except ValueError:
        send_message(chat_id, "❌ ID invalide")

# === STOCK HANDLERS ===

def handle_stock(chat_id):
    stock = get_all_stock()
    
    trackers = [s for s in stock if s['product_type'] == 'tracker']
    nylon = [s for s in stock if s['product_type'] == 'nylon']
    silicone = [s for s in stock if s['product_type'] == 'silicone']
    
    def format_qty(qty, threshold=3):
        if qty == 0:
            return f"{qty} 🔴"
        elif qty <= threshold:
            return f"{qty} ⚠️"
        return str(qty)
    
    text = "📦 <b>STOCK GUINDIMA</b>\n\n"
    
    # Trackers
    text += "🔌 <b>Trackers :</b>\n"
    for t in trackers:
        text += f"  • Tracker GPS : {format_qty(t['quantity'])}\n"
    
    # Nylon
    text += "\n🎨 <b>Bracelets Nylon :</b>\n"
    for n in nylon:
        text += f"  • {n['variant_name']} (<code>{n['variant_code']}</code>) : {format_qty(n['quantity'])}\n"
    
    # Silicone
    text += "\n🦄 <b>Bracelets Silicone :</b>\n"
    for s in silicone:
        text += f"  • {s['variant_name']} (<code>{s['variant_code']}</code>) : {format_qty(s['quantity'])}\n"
    
    send_message(chat_id, text)

def handle_lowstock(chat_id):
    low = get_low_stock()
    
    if not low:
        send_message(chat_id, "✅ Tout le stock est OK !")
        return
    
    text = "⚠️ <b>STOCK FAIBLE / RUPTURE</b>\n\n"
    for item in low:
        name = item['variant_name'] or 'Tracker GPS'
        code = item['variant_code'] or 'T'
        qty = item['quantity']
        status = "🔴 RUPTURE" if qty == 0 else "⚠️ FAIBLE"
        text += f"  • {name} (<code>{code}</code>) : {qty} {status}\n"
    
    send_message(chat_id, text)

def handle_stock_add(chat_id, args):
    """Format: /s+ T 10 ou /s+ BN:nr 5"""
    try:
        parts = args.strip().split()
        if len(parts) < 2:
            send_message(chat_id, "❌ Format: /s+ PRODUIT QUANTITE\nEx: /s+ T 10 ou /s+ BN:nr 5")
            return
        
        product = parts[0].upper()
        qty = int(parts[1])
        
        if ':' in product:
            # Bracelet avec variante
            code, variant = product.split(':', 1)
            variant = variant.lower()
            
            if code == 'BN':
                if variant not in NYLON_COLORS:
                    send_message(chat_id, f"❌ Couleur Nylon inconnue: {variant}")
                    return
                result = update_stock('nylon', variant, qty, 'add')
                name = NYLON_COLORS[variant]
            elif code == 'BS':
                if variant not in SILICONE_DESIGNS:
                    send_message(chat_id, f"❌ Motif Silicone inconnu: {variant}")
                    return
                result = update_stock('silicone', variant, qty, 'add')
                name = SILICONE_DESIGNS[variant]
            else:
                send_message(chat_id, f"❌ Code produit invalide: {code}")
                return
        else:
            # Tracker
            if product == 'T':
                result = update_stock('tracker', None, qty, 'add')
                name = 'Tracker GPS'
            else:
                send_message(chat_id, f"❌ Code produit invalide: {product}")
                return
        
        if result:
            send_message(chat_id, f"✅ Stock mis à jour\n\n{name} : +{qty} → <b>{result['quantity']}</b> total")
        else:
            send_message(chat_id, "❌ Erreur mise à jour stock")
    
    except ValueError:
        send_message(chat_id, "❌ Quantité invalide")

def handle_stock_sub(chat_id, args):
    """Format: /s- T 10 ou /s- BN:nr 5"""
    try:
        parts = args.strip().split()
        if len(parts) < 2:
            send_message(chat_id, "❌ Format: /s- PRODUIT QUANTITE\nEx: /s- T 10 ou /s- BN:nr 5")
            return
        
        product = parts[0].upper()
        qty = int(parts[1])
        
        if ':' in product:
            code, variant = product.split(':', 1)
            variant = variant.lower()
            
            if code == 'BN':
                if variant not in NYLON_COLORS:
                    send_message(chat_id, f"❌ Couleur Nylon inconnue: {variant}")
                    return
                result = update_stock('nylon', variant, qty, 'sub')
                name = NYLON_COLORS[variant]
            elif code == 'BS':
                if variant not in SILICONE_DESIGNS:
                    send_message(chat_id, f"❌ Motif Silicone inconnu: {variant}")
                    return
                result = update_stock('silicone', variant, qty, 'sub')
                name = SILICONE_DESIGNS[variant]
            else:
                send_message(chat_id, f"❌ Code produit invalide: {code}")
                return
        else:
            if product == 'T':
                result = update_stock('tracker', None, qty, 'sub')
                name = 'Tracker GPS'
            else:
                send_message(chat_id, f"❌ Code produit invalide: {product}")
                return
        
        if result:
            send_message(chat_id, f"✅ Stock mis à jour\n\n{name} : -{qty} → <b>{result['quantity']}</b> total")
        else:
            send_message(chat_id, "❌ Erreur mise à jour stock")
    
    except ValueError:
        send_message(chat_id, "❌ Quantité invalide")

def handle_stock_set(chat_id, args):
    """Format: /s= T 20 ou /s= BN:nr 10"""
    try:
        parts = args.strip().split()
        if len(parts) < 2:
            send_message(chat_id, "❌ Format: /s= PRODUIT QUANTITE\nEx: /s= T 20 ou /s= BN:nr 10")
            return
        
        product = parts[0].upper()
        qty = int(parts[1])
        
        if ':' in product:
            code, variant = product.split(':', 1)
            variant = variant.lower()
            
            if code == 'BN':
                if variant not in NYLON_COLORS:
                    send_message(chat_id, f"❌ Couleur Nylon inconnue: {variant}")
                    return
                result = update_stock('nylon', variant, qty, 'set')
                name = NYLON_COLORS[variant]
            elif code == 'BS':
                if variant not in SILICONE_DESIGNS:
                    send_message(chat_id, f"❌ Motif Silicone inconnu: {variant}")
                    return
                result = update_stock('silicone', variant, qty, 'set')
                name = SILICONE_DESIGNS[variant]
            else:
                send_message(chat_id, f"❌ Code produit invalide: {code}")
                return
        else:
            if product == 'T':
                result = update_stock('tracker', None, qty, 'set')
                name = 'Tracker GPS'
            else:
                send_message(chat_id, f"❌ Code produit invalide: {product}")
                return
        
        if result:
            send_message(chat_id, f"✅ Stock défini\n\n{name} : <b>{result['quantity']}</b>")
        else:
            send_message(chat_id, "❌ Erreur mise à jour stock")
    
    except ValueError:
        send_message(chat_id, "❌ Quantité invalide")

# === MAIN HANDLER ===

def process_update(update):
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')
    
    if not chat_id or not text:
        return
    
    if str(chat_id) != str(Config.TELEGRAM_ADMIN_CHAT_ID):
        send_message(chat_id, "⛔ Accès non autorisé.")
        return
    
    text = text.strip()
    
    if text == '/start':
        handle_start(chat_id)
    elif text == '/aide' or text == '/help':
        handle_aide(chat_id)
    elif text.startswith('/cmd '):
        handle_cmd(chat_id, text)
    elif text == '/list':
        handle_list(chat_id)
    elif text == '/today':
        handle_today(chat_id)
    elif text.startswith('/find '):
        handle_find(chat_id, text.replace('/find ', '').strip())
    elif text == '/stats':
        handle_stats(chat_id)
    elif text.startswith('/acompte '):
        handle_acompte(chat_id, text.replace('/acompte ', '').strip())
    elif text.startswith('/pay '):
        handle_pay(chat_id, text.replace('/pay ', '').strip())
    elif text.startswith('/ship '):
        handle_ship(chat_id, text.replace('/ship ', '').strip())
    elif text.startswith('/done '):
        handle_done(chat_id, text.replace('/done ', '').strip())
    elif text.startswith('/show '):
        handle_show(chat_id, text.replace('/show ', '').strip())
    elif text.startswith('/del '):
        handle_del(chat_id, text.replace('/del ', '').strip())
    elif text.startswith('/edit '):
        handle_edit(chat_id, text.replace('/edit ', '').strip())
    elif text.startswith('/cancel '):
        handle_cancel(chat_id, text.replace('/cancel ', '').strip())
    elif text == '/stock':
        handle_stock(chat_id)
    elif text == '/lowstock':
        handle_lowstock(chat_id)
    elif text.startswith('/s+ '):
        handle_stock_add(chat_id, text.replace('/s+ ', '').strip())
    elif text.startswith('/s- '):
        handle_stock_sub(chat_id, text.replace('/s- ', '').strip())
    elif text.startswith('/s= '):
        handle_stock_set(chat_id, text.replace('/s= ', '').strip())
    elif text.startswith('#'):
        handle_show(chat_id, text.replace('#', '').strip())
    else:
        send_message(chat_id, "🤔 Commande non reconnue. Tape /aide pour voir les commandes.")

if __name__ == '__main__':
    print("Bot module loaded")
