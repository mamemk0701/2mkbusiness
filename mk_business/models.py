import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db():
    return psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    # Supprimer les anciennes tables si elles existent
    cur.execute('DROP TABLE IF EXISTS order_items CASCADE')
    cur.execute('DROP TABLE IF EXISTS orders CASCADE')
    cur.execute('DROP TABLE IF EXISTS clients CASCADE')
    cur.execute('DROP TABLE IF EXISTS conversations CASCADE')
    cur.execute('DROP TABLE IF EXISTS escalations CASCADE')
    
    # Table clients
    cur.execute('''
        CREATE TABLE clients (
            id SERIAL PRIMARY KEY,
            phone VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table commandes
    cur.execute('''
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            total INTEGER DEFAULT 0,
            acompte INTEGER DEFAULT 0,
            payment_status VARCHAR(20) DEFAULT 'pending',
            delivery_status VARCHAR(20) DEFAULT 'preparation',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table articles de commande
    cur.execute('''
        CREATE TABLE order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            product_code VARCHAR(10) NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            variant VARCHAR(50),
            quantity INTEGER DEFAULT 1,
            unit_price INTEGER NOT NULL,
            subtotal INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized")

# === FONCTIONS CLIENTS ===

def get_or_create_client(phone, name=None, address=None):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM clients WHERE phone = %s", (phone,))
    client = cur.fetchone()
    
    if not client:
        cur.execute(
            "INSERT INTO clients (phone, name, address) VALUES (%s, %s, %s) RETURNING *",
            (phone, name, address)
        )
        client = cur.fetchone()
        conn.commit()
    elif name or address:
        cur.execute(
            "UPDATE clients SET name = COALESCE(%s, name), address = COALESCE(%s, address) WHERE id = %s RETURNING *",
            (name, address, client['id'])
        )
        client = cur.fetchone()
        conn.commit()
    
    cur.close()
    conn.close()
    return client

# === FONCTIONS COMMANDES ===

def create_order(client_id, items, total):
    conn = get_db()
    cur = conn.cursor()
    
    # Créer la commande
    cur.execute(
        "INSERT INTO orders (client_id, total) VALUES (%s, %s) RETURNING *",
        (client_id, total)
    )
    order = cur.fetchone()
    
    # Ajouter les articles
    for item in items:
        cur.execute(
            """INSERT INTO order_items 
               (order_id, product_code, product_name, variant, quantity, unit_price, subtotal) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (order['id'], item['code'], item['name'], item.get('variant'), 
             item['quantity'], item['unit_price'], item['subtotal'])
        )
    
    conn.commit()
    cur.close()
    conn.close()
    return order

def get_order(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.*, c.name as client_name, c.phone as client_phone, c.address as client_address
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE o.id = %s
    """, (order_id,))
    order = cur.fetchone()
    
    if order:
        cur.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
        order['items'] = cur.fetchall()
    
    cur.close()
    conn.close()
    return order

def get_orders_by_status(payment_status=None, delivery_status=None):
    conn = get_db()
    cur = conn.cursor()
    
    query = """
        SELECT o.*, c.name as client_name, c.phone as client_phone, c.address as client_address
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE 1=1
    """
    params = []
    
    if payment_status:
        query += " AND o.payment_status = %s"
        params.append(payment_status)
    if delivery_status:
        query += " AND o.delivery_status = %s"
        params.append(delivery_status)
    
    query += " ORDER BY o.created_at DESC"
    
    cur.execute(query, params)
    orders = cur.fetchall()
    
    cur.close()
    conn.close()
    return orders

def get_pending_orders():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.*, c.name as client_name, c.phone as client_phone, c.address as client_address
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE o.delivery_status != 'delivered'
        ORDER BY o.created_at DESC
    """)
    orders = cur.fetchall()
    
    cur.close()
    conn.close()
    return orders

def get_today_orders():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.*, c.name as client_name, c.phone as client_phone, c.address as client_address
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE DATE(o.created_at) = CURRENT_DATE
        ORDER BY o.created_at DESC
    """)
    orders = cur.fetchall()
    
    cur.close()
    conn.close()
    return orders

def search_orders_by_phone(phone):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.*, c.name as client_name, c.phone as client_phone, c.address as client_address
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE c.phone LIKE %s
        ORDER BY o.created_at DESC
    """, (f'%{phone}%',))
    orders = cur.fetchall()
    
    cur.close()
    conn.close()
    return orders

def update_order_acompte(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE orders SET acompte = 2000, payment_status = 'acompte', updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
        (order_id,)
    )
    order = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return order

def update_order_paid(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE orders 
        SET acompte = total, payment_status = 'paid', updated_at = CURRENT_TIMESTAMP 
        WHERE id = %s RETURNING *
    """, (order_id,))
    order = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return order

def update_order_shipping(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE orders SET delivery_status = 'shipping', updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
        (order_id,)
    )
    order = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return order

def update_order_delivered(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE orders SET delivery_status = 'delivered', updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
        (order_id,)
    )
    order = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return order

def get_stats():
    conn = get_db()
    cur = conn.cursor()
    
    # Stats globales
    cur.execute("SELECT COUNT(*) as total_orders, COALESCE(SUM(total), 0) as total_revenue FROM orders")
    global_stats = cur.fetchone()
    
    # Stats du jour
    cur.execute("""
        SELECT COUNT(*) as today_orders, COALESCE(SUM(total), 0) as today_revenue 
        FROM orders WHERE DATE(created_at) = CURRENT_DATE
    """)
    today_stats = cur.fetchone()
    
    # Commandes en attente
    cur.execute("SELECT COUNT(*) as pending FROM orders WHERE delivery_status != 'delivered'")
    pending = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return {
        'total_orders': global_stats['total_orders'],
        'total_revenue': global_stats['total_revenue'],
        'today_orders': today_stats['today_orders'],
        'today_revenue': today_stats['today_revenue'],
        'pending_orders': pending['pending']
    }

if __name__ == '__main__':
    init_db()

def delete_order(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    cur.execute("DELETE FROM orders WHERE id = %s RETURNING id", (order_id,))
    deleted = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return deleted is not None

def update_client_info(order_id, field, value):
    conn = get_db()
    cur = conn.cursor()
    
    # Récupérer le client_id de la commande
    cur.execute("SELECT client_id FROM orders WHERE id = %s", (order_id,))
    order = cur.fetchone()
    
    if not order:
        cur.close()
        conn.close()
        return False
    
    client_id = order['client_id']
    
    if field == 'name':
        cur.execute("UPDATE clients SET name = %s WHERE id = %s", (value, client_id))
    elif field == 'phone':
        cur.execute("UPDATE clients SET phone = %s WHERE id = %s", (value, client_id))
    elif field == 'address':
        cur.execute("UPDATE clients SET address = %s WHERE id = %s", (value, client_id))
    else:
        cur.close()
        conn.close()
        return False
    
    conn.commit()
    cur.close()
    conn.close()
    return True

def cancel_order(order_id):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE orders SET delivery_status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
        (order_id,)
    )
    order = cur.fetchone()
    conn.commit()
    
    cur.close()
    conn.close()
    return order

# === STOCK FUNCTIONS ===

def init_stock():
    """Initialise la table stock"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('DROP TABLE IF EXISTS stock CASCADE')
    
    cur.execute('''
        CREATE TABLE stock (
            id SERIAL PRIMARY KEY,
            product_type VARCHAR(20) NOT NULL,
            variant_code VARCHAR(20),
            variant_name VARCHAR(100),
            quantity INTEGER DEFAULT 0,
            alert_threshold INTEGER DEFAULT 3,
            UNIQUE(product_type, variant_code)
        )
    ''')
    
    # Insérer les produits de base
    # Tracker
    cur.execute("INSERT INTO stock (product_type, variant_code, variant_name, quantity) VALUES ('tracker', NULL, 'Tracker GPS', 0)")
    
    # Bracelets Nylon
    nylon = [
        ('nr', 'Noir'), ('rg', 'Rouge'), ('rb', 'Rainbow'), ('7c', 'Sept couleurs'),
        ('jv', 'Jaune-Vert'), ('bl', 'Bleu'), ('bc', 'Blanc coquille'), ('rs', 'Rose sable')
    ]
    for code, name in nylon:
        cur.execute("INSERT INTO stock (product_type, variant_code, variant_name, quantity) VALUES ('nylon', %s, %s, 0)", (code, name))
    
    # Bracelets Silicone
    silicone = [
        ('lic1', 'Licorne café (violet)'), ('lic2', 'Licorne tête (gris)'), ('lic3', 'Licorne ailée (rose)'),
        ('gla', 'Glace (blanc)'), ('don1', 'Donut licorne (jaune)'), ('don2', 'Donut noeud (rouge)'),
        ('bal', 'Baleine (fuchsia)'), ('suc', 'Sucettes (vert fluo)'), ('cup', 'Cupcake (turquoise)'),
        ('din1', 'Dino fraise (vert pastel)'), ('din2', 'Dino bébé (bleu gris)'), ('nua', 'Nuage (menthe)'),
        ('arc', 'Arc-en-ciel (rose clair)'), ('sat', 'Saturne (bleu marine)'), ('fle', 'Fleur (noir)')
    ]
    for code, name in silicone:
        cur.execute("INSERT INTO stock (product_type, variant_code, variant_name, quantity) VALUES ('silicone', %s, %s, 0)", (code, name))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Stock table initialized")

def get_stock_item(product_type, variant_code=None):
    conn = get_db()
    cur = conn.cursor()
    
    if variant_code:
        cur.execute("SELECT * FROM stock WHERE product_type = %s AND variant_code = %s", (product_type, variant_code))
    else:
        cur.execute("SELECT * FROM stock WHERE product_type = %s AND variant_code IS NULL", (product_type,))
    
    item = cur.fetchone()
    cur.close()
    conn.close()
    return item

def get_all_stock():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM stock ORDER BY product_type, variant_code")
    items = cur.fetchall()
    
    cur.close()
    conn.close()
    return items

def get_low_stock(threshold=None):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM stock WHERE quantity <= COALESCE(%s, alert_threshold) ORDER BY quantity ASC", (threshold,))
    items = cur.fetchall()
    
    cur.close()
    conn.close()
    return items

def update_stock(product_type, variant_code, quantity, mode='set'):
    """
    mode: 'set' = définir la quantité
          'add' = ajouter à la quantité
          'sub' = soustraire de la quantité
    """
    conn = get_db()
    cur = conn.cursor()
    
    if mode == 'set':
        if variant_code:
            cur.execute("UPDATE stock SET quantity = %s WHERE product_type = %s AND variant_code = %s RETURNING *", 
                       (quantity, product_type, variant_code))
        else:
            cur.execute("UPDATE stock SET quantity = %s WHERE product_type = %s AND variant_code IS NULL RETURNING *", 
                       (quantity, product_type))
    elif mode == 'add':
        if variant_code:
            cur.execute("UPDATE stock SET quantity = quantity + %s WHERE product_type = %s AND variant_code = %s RETURNING *", 
                       (quantity, product_type, variant_code))
        else:
            cur.execute("UPDATE stock SET quantity = quantity + %s WHERE product_type = %s AND variant_code IS NULL RETURNING *", 
                       (quantity, product_type))
    elif mode == 'sub':
        if variant_code:
            cur.execute("UPDATE stock SET quantity = quantity - %s WHERE product_type = %s AND variant_code = %s RETURNING *", 
                       (quantity, product_type, variant_code))
        else:
            cur.execute("UPDATE stock SET quantity = quantity - %s WHERE product_type = %s AND variant_code IS NULL RETURNING *", 
                       (quantity, product_type))
    
    item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return item

def check_stock_availability(items):
    """
    Vérifie si le stock est suffisant pour une commande
    Retourne (True, []) si OK, (False, [liste des problèmes]) sinon
    """
    problems = []
    stock_needed = {}  # {(type, variant): quantity_needed}
    
    for item in items:
        code = item['code']
        variant = item.get('variant_code')
        qty = item.get('quantity', 1)
        
        # Tracker seul
        if code == 'T':
            key = ('tracker', None)
            stock_needed[key] = stock_needed.get(key, 0) + qty
        
        # Bracelet Nylon seul
        elif code == 'BN':
            key = ('nylon', variant)
            stock_needed[key] = stock_needed.get(key, 0) + qty
        
        # Bracelet Silicone seul
        elif code == 'BS':
            key = ('silicone', variant)
            stock_needed[key] = stock_needed.get(key, 0) + qty
        
        # Kit Saytu = Tracker + Silicone
        elif code == 'KS':
            key_tracker = ('tracker', None)
            key_silicone = ('silicone', variant)
            stock_needed[key_tracker] = stock_needed.get(key_tracker, 0) + qty
            stock_needed[key_silicone] = stock_needed.get(key_silicone, 0) + qty
        
        # Kit Guëstu = Tracker + Nylon
        elif code == 'KG':
            key_tracker = ('tracker', None)
            key_nylon = ('nylon', variant)
            stock_needed[key_tracker] = stock_needed.get(key_tracker, 0) + qty
            stock_needed[key_nylon] = stock_needed.get(key_nylon, 0) + qty
    
    # Vérifier chaque item
    for (product_type, variant_code), needed in stock_needed.items():
        stock_item = get_stock_item(product_type, variant_code)
        if not stock_item:
            problems.append(f"Produit inconnu: {product_type}/{variant_code}")
        elif stock_item['quantity'] < needed:
            problems.append(f"{stock_item['variant_name'] or 'Tracker'}: {stock_item['quantity']} dispo, {needed} demandé")
    
    return (len(problems) == 0, problems)

def deduct_stock_for_order(items):
    """Déduit le stock après une commande confirmée"""
    for item in items:
        code = item['code']
        variant = item.get('variant_code')
        qty = item.get('quantity', 1)
        
        if code == 'T':
            update_stock('tracker', None, qty, 'sub')
        
        elif code == 'BN':
            update_stock('nylon', variant, qty, 'sub')
        
        elif code == 'BS':
            update_stock('silicone', variant, qty, 'sub')
        
        elif code == 'KS':
            update_stock('tracker', None, qty, 'sub')
            update_stock('silicone', variant, qty, 'sub')
        
        elif code == 'KG':
            update_stock('tracker', None, qty, 'sub')
            update_stock('nylon', variant, qty, 'sub')

def restore_stock_for_order(order_id):
    """Restaure le stock si commande annulée/supprimée"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
    items = cur.fetchall()
    
    cur.close()
    conn.close()
    
    for item in items:
        code = item['product_code']
        variant = item.get('variant')
        qty = item['quantity']
        
        # Retrouver le variant_code depuis le variant_name
        variant_code = None
        if variant:
            # Chercher dans les dictionnaires
            from config import NYLON_COLORS, SILICONE_DESIGNS
            for k, v in NYLON_COLORS.items():
                if v == variant:
                    variant_code = k
                    break
            if not variant_code:
                for k, v in SILICONE_DESIGNS.items():
                    if v == variant:
                        variant_code = k
                        break
        
        if code == 'T':
            update_stock('tracker', None, qty, 'add')
        elif code == 'BN':
            update_stock('nylon', variant_code, qty, 'add')
        elif code == 'BS':
            update_stock('silicone', variant_code, qty, 'add')
        elif code == 'KS':
            update_stock('tracker', None, qty, 'add')
            update_stock('silicone', variant_code, qty, 'add')
        elif code == 'KG':
            update_stock('tracker', None, qty, 'add')
            update_stock('nylon', variant_code, qty, 'add')
