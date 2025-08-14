import sqlite3
import re

DB_FILE = 'scraped_data.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def setup_database():
    conn = get_connection()
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS items")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            link TEXT UNIQUE,
            source TEXT,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def parse_price(price_str):
    if not price_str:
        return None

    # Remove commas
    price_str = price_str.replace(',', '')

    # Find the first number in the string
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group())
    return None



def insert_items_bulk(items):
    conn = get_connection()
    cur = conn.cursor()

    data_to_insert = [
        (item['title'], parse_price(item['price']), item['link'], item['source'])
        for item in items
    ]

    cur.executemany(
        "INSERT OR REPLACE INTO items (title, price, link, source) VALUES (?, ?, ?, ?)",
        data_to_insert
    )

    conn.commit()
    conn.close()
