import sqlite3

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