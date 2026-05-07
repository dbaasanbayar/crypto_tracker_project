import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()



def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if DATABASE_URL is None:
        print("❌ АЛДАА: DATABASE_URL хувьсагч огт олдохгүй байна!")
    else:
        print(f"📡 DATABASE_URL олдлоо. Урт нь: {len(DATABASE_URL)} тэмдэгт.")
        # Нууцлалын үүднээс зөвхөн эхлэлийг нь харна
        print(f"🔗 URL эхлэл: {DATABASE_URL[:15]}...")

    return psycopg2.connect(DATABASE_URL, sslmode='require')

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Assets хүснэгт (SERIAL ашиглана)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    # 2. Price History хүснэгт
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id SERIAL PRIMARY KEY,
            asset_id INTEGER REFERENCES assets(id),
            price DECIMAL NOT NULL,
            timestamp BIGINT NOT NULL
        )
    ''')
    
    # 3. Hourly Summary хүснэгт
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hourly_summary(
            id SERIAL PRIMARY KEY,
            asset_id INTEGER REFERENCES assets(id),
            avg_price DECIMAL,
            max_price DECIMAL,
            min_price DECIMAL,
            hour_timestamp TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("🗄️ Neon PostgreSQL бүтэц бэлэн боллоо.")

def save_to_db(coin_data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for coin in coin_data:
            # ON CONFLICT ашиглан давхардахаас сэргийлнэ
            cursor.execute('''
                INSERT INTO assets (symbol, name) 
                VALUES (%s, %s)
                ON CONFLICT (symbol) DO NOTHING
            ''', (coin['symbol'], coin['name']))
            
            cursor.execute('SELECT id FROM assets WHERE symbol = %s', (coin['symbol'],))
            asset_id = cursor.fetchone()[0]

            cursor.execute('''
                INSERT INTO price_history (asset_id, price, timestamp)
                VALUES (%s, %s, %s)
            ''', (asset_id, coin['price'], coin['timestamp']))
            
        conn.commit()
        print("✅ Дата Neon руу амжилттай хадгалагдлаа!")
    except Exception as e:
        print(f"❌ Алдаа гарлаа: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()