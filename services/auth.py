import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "grocery.db")

def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None
