import sqlite3
<<<<<<< HEAD
import os

def create_tables(db='data/crypto.db'):
    os.makedirs(os.path.dirname(db), exist_ok=True)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # 1. Assets хүснэгт (Parent Table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    # 2. Price History хүснэгт (Child Table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            price REAL NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES assets (id)
        )
    ''')
    
    conn.commit()
    conn.close()
=======
>>>>>>> 2c5a62abd813c2eb0b48428309ed2e455ce6c0e3

def save_to_db(coin_data):
    # 'with' ашигласнаар conn.close() хийх шаардлагагүй, автоматаар хаагдана
    with sqlite3.connect("data/crypto.db") as conn:
        cursor = conn.cursor()
<<<<<<< HEAD
    
=======

>>>>>>> 2c5a62abd813c2eb0b48428309ed2e455ce6c0e3
        for coin in coin_data:
            # 1. Зоос assets хүснэгтэд байгаа эсэхийг шалгах, байхгүй бол нэмэх
            # 'symbol' багана UNIQUE учраас INSERT OR IGNORE давхардахаас сэргийлнэ
            cursor.execute('''
                INSERT OR IGNORE INTO assets (symbol, name) 
                VALUES (?, ?)
            ''', (coin['symbol'], coin['name']))
<<<<<<< HEAD
            
=======

>>>>>>> 2c5a62abd813c2eb0b48428309ed2e455ce6c0e3
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