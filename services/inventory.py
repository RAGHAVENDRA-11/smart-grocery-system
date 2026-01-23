import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "grocery.db")

def add_product(name, category, aisle, price, stock):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, category, aisle, price, stock)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, aisle, price, stock))

    conn.commit()
    conn.close()
    print("🛒 Product added successfully!")

def view_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()
    return products

def search_product(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, aisle, price, stock
        FROM products
        WHERE name LIKE ?
    """, ('%' + name + '%',))

    result = cursor.fetchall()
    conn.close()
    return result
