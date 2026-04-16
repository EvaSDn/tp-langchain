#sql lite on peut utiliser pout le projet 
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            nom TEXT,
            email TEXT,
            ville TEXT,
            solde_compte REAL,
            type_compte TEXT,
            date_inscription TEXT,
            achats_total REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id TEXT PRIMARY KEY,
            nom TEXT,
            prix_ht REAL,
            tva REAL DEFAULT 0.20,
            stock INTEGER
        )
    """)

    clients = [
        ("C001", "Marie Dupont", "marie.dupont@email.fr", "Paris", 15420.50, "Premium", "2021-03-15", 8750.00),
        ("C002", "Jean Martin", None, None, 3200.00, "Standard", None, None),
        ("C003", "Sophie Bernard", None, None, 28900.00, "VIP", None, None),
        ("C004", "Lucas Petit", None, None, 750.00, "Standard", None, None),
    ]
    for c in clients:
        cur.execute("INSERT INTO clients VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", c)

    produits = [
        ("P001", "Ordinateur portable Pro", 899.00, 0.20, 45),
        ("P002", "Souris ergonomique", 49.90, 0.20, 120),
        ("P003", "Bureau réglable", 350.00, 0.20, 18),
        ("P004", "Casque audio sans fil", 129.00, 0.20, 67),
        ("P005", "Écran 27 pouces 4K", 549.00, 0.20, 30),
    ]
    for p in produits:
        cur.execute("INSERT INTO produits VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING", p)


    conn.commit()
    cur.close()
    conn.close()

init_db()

def rechercher_client(query: str) -> str:
    query = query.strip()
    connexion = get_connection()
    cur = connexion.cursor()

    cur.execute("SELECT * FROM clients WHERE UPPER(id) = %s", (query.upper(),))
    row = cur.fetchone()

    if not row:
        cur.execute("SELECT * FROM clients WHERE LOWER(nom) LIKE %s", (f"%{query.lower()}%",))
        row = cur.fetchone()

    cur.close()
    connexion.close()
    if row:
        return f"Client : {row[1]} | Solde : {row[4]:.2f} € | Type de compte : {row[5]}"
    return f"Aucun client trouvé pour : '{query}'"



def rechercher_produit(query: str) -> str:
    query = query.strip()
    connexion = get_connection()
    cur = connexion.cursor()

    cur.execute("SELECT * FROM produits WHERE UPPER(id) = %s", (query.upper(),))
    row = cur.fetchone()

    if not row:
        cur.execute("SELECT * FROM produits WHERE LOWER(nom) LIKE %s", (f"%{query.lower()}%",))
        row = cur.fetchone()

    cur.close()
    connexion.close()
    if row:
        tva = row[2] * row[3]
        prix_ttc = row[2] + tva
        return (f"Produit : {row[1]} | Prix HT : {row[2]:.2f} € "
                f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {row[4]}")
    return f"Aucun produit trouvé pour : '{query}'"

def lister_tous_les_clients(query: str = "") -> str:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, type_compte, solde_compte FROM clients")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = "Liste des clients :\n"
    for row in rows:
        result += f"  {row[0]} : {row[1]} | {row[2]} | Solde : {row[3]:.2f} €\n"
    return result