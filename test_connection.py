import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# 1. DATABASE_URL байгаа эсэхийг шалгах
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ АЛДАА: .env файл дотор DATABASE_URL олдохгүй байна!")
    exit()

print("🚀 Neon руу холбогдож байна...")

try:
    # 2. Холболт тогтоох (SSL заавал хэрэгтэй)
    conn = psycopg2.connect(db_url, sslmode='require')
    cursor = conn.cursor()
    
    # 3. Холболтыг шалгах (Server-ийн цагийг асуух)
    cursor.execute("SELECT now();")
    db_time = cursor.fetchone()
    print(f"✅ Холболт амжилттай! Серверийн цаг: {db_time[0]}")

    # 4. Анхны хүснэгт үүсгэх тест
    print("👷 Хүснэгт үүсгэж байна...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("✅ 'assets' хүснэгт амжилттай үүсэв.")

    cursor.close()
    conn.close()
    print("🏁 Тест амжилттай дууслаа.")

except Exception as e:
    print(f"❌ Холболтонд алдаа гарлаа: {e}")