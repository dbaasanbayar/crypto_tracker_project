import sqlite3
import os

# Өгөгдлийн сангийн байршил
DB_PATH = 'data/crypto.db'

def get_connection():
    """Өгөгдлийн сантай холбогдох холболтыг буцаана."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Foreign key дэмжлэгийг идэвхжүүлэх (SQLite-д заавал ингэж зааж өгдөг)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    """Хэрэгцээт бүх хүснэгтүүдийг үүсгэнэ."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Assets хүснэгт
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    # 2. Price History хүснэгт (Түүхий өгөгдөл)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            price REAL NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        )
    ''')
    
    # 3. Hourly Summary хүснэгт (Боловсруулсан өгөгдөл)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hourly_summary(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            avg_price REAL,
            max_price REAL,
            min_price REAL,
            hour_timestamp TEXT,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Өгөгдлийн сангийн бүтэц бэлэн боллоо.")

def save_to_db(coin_data):
    # 'with' ашигласнаар conn.close() хийх шаардлагагүй, автоматаар хаагдана
    with sqlite3.connect("data/crypto.db") as conn:
        cursor = conn.cursor()
        for coin in coin_data:
            # 1. Зоос assets хүснэгтэд байгаа эсэхийг шалгах, байхгүй бол нэмэх
            # 'symbol' багана UNIQUE учраас INSERT OR IGNORE давхардахаас сэргийлнэ
            cursor.execute('''
                INSERT OR IGNORE INTO assets (symbol, name) 
                VALUES (?, ?)
            ''', (coin['symbol'], coin['name']))
            # 2. Тухайн зоосны ID-г олж авах (Lookup)
            cursor.execute('SELECT id FROM assets WHERE symbol = ?', (coin['symbol'],))
            asset_id = cursor.fetchone()[0]

            # 3. Олж авсан asset_id-г ашиглан ханшийг түүх рүү хадгалах
            cursor.execute('''
                INSERT INTO price_history (asset_id, price, timestamp)
                VALUES (?, ?, ?)
            ''', (asset_id, coin['price'], coin['timestamp']))
            
        conn.commit()
    print("Дата амжилттай хадгалагдлаа!")