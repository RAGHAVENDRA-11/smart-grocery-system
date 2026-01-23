import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "grocery.db")

def place_order(customer_id, product_id, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT price, stock FROM products WHERE product_id=?",
        (product_id,)
    )
    product = cursor.fetchone()

    if not product:
        print("❌ Product not found")
        return

    price, stock = product

    if stock < quantity:
        print("❌ Not enough stock available")
        return

    total_price = price * quantity

    cursor.execute("""
        INSERT INTO orders (customer_id, product_id, quantity, total_price, status)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, product_id, quantity, total_price, "PAID"))

    cursor.execute("""
        UPDATE products
        SET stock = stock - ?
        WHERE product_id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()

    print(f"✅ Order placed! Amount paid: ₹{total_price}")
