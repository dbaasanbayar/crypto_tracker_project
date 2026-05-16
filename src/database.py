import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("❌ DATABASE_URL environment variable тохируулагдаагүй байна!")

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    return psycopg2.connect(DATABASE_URL, sslmode='require')
    
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
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
        CREATE TABLE IF NOT EXISTS hourly_summary (
        id SERIAL PRIMARY KEY,
        asset_id INTEGER REFERENCES assets(id),
        avg_price DECIMAL,
        max_price DECIMAL,
        min_price DECIMAL,
        hour_timestamp TIMESTAMP,

        -- ✅ Нэмэх: нэг зоос, нэг цагт ганцхан мөр байна
        UNIQUE(asset_id, hour_timestamp)
    )
    ''') 
        conn.commit()
        print("🗄️ Neon PostgreSQL бүтэц бэлэн боллоо.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Хүснэгт үүсгэхэд алдаа: {e}")
        raise
    finally:     
        cursor.close()
        conn.close()

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

def get_recent_prices(hours=24):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT a.symbol, ph.price, ph.timestamp
        FROM price_history ph
        JOIN assets a ON ph.asset_id = a.id
        WHERE ph.timestamp >= (EXTRACT(EPOCH FROM NOW()) - %s) * 1000
        ORDER BY ph.timestamp DESC
    """
    
    try:
        cur.execute(query, (hours * 3600,))
        rows = cur.fetchall()

        data_str = ""
        for row in rows:
            data_str += f"Coin: {row[0]}, Price: ${row[1]:,.2f}, Time: {row[2]}\n"
        return data_str
    except Exception as e:
        print(f"❌ Query алдаа: {e}")
        return ""
    finally:
        cur.close()
        conn.close()
def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Алхам 1: Давхардсан мөрүүдийг устгах
        cursor.execute("""
            DELETE FROM hourly_summary a
            USING hourly_summary b
            WHERE a.id > b.id
                AND a.asset_id = b.asset_id
                AND a.hour_timestamp = b.hour_timestamp;
        """)
        print(f"🧹 Давхардсан мөрүүд устгагдлаа.")

        cursor.execute("""
            ALTER TABLE hourly_summary 
            ADD CONSTRAINT hourly_summary_unique 
            UNIQUE (asset_id, hour_timestamp);
        """)
        print("✅ UNIQUE constraint амжилттай нэмэгдлээ.")

        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"ℹ️  Migration: {e}")  # аль хэдийн байвал алдаа биш
    finally:
        cursor.close()
        conn.close()