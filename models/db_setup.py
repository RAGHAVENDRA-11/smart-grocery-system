import sqlite3
import os

def create_database():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_DIR = os.path.join(BASE_DIR, "database")
    os.makedirs(DB_DIR, exist_ok=True)

    DB_PATH = os.path.join(DB_DIR, "grocery.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        aisle TEXT,
        price REAL,
        stock INTEGER
    )
    """)

    # Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT
    )
    """)

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        status TEXT
    )
    """)

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Insert default users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("customer", "cust123", "customer")
        )

    conn.commit()
    conn.close()

    print("✅ Database created with users, products, orders")

if __name__ == "__main__":
    create_database()
