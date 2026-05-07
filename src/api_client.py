import requests
import os
from dotenv import load_dotenv

# 1. .env файлыг уншиж эхлүүлэх
load_dotenv()
# 2. Түлхүүрийг орчны хувьсагчаас татаж авах
# Хэрэв олдохгүй бол None буцаана
COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")

def fetch_prices():
    url = "https://rest.coincap.io/v3/assets"

    # Түлхүүр байхгүй бол анхааруулга өгөх
    if not COINCAP_API_KEY:
        print("Алдаа: COINCAP_API_KEY олдсонгүй. .env файлаа шалгана уу.")
        return []
    
    headers = {
                "Authorization": f"Bearer {COINCAP_API_KEY}",
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
    
    try: 
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Хэрэв 404 эсвэл 500 алдаа гарвал шууд except рүү үсрэнэ
        
        full_data = response.json() # Бүх датаг авах
        all_coins = full_data['data'] # 'data' түлхүүр доторх жагсаалтыг авах
        
        clean_data = []
        # Зөвхөн эхний 10 зоосыг туршилтаар авъя
        for coin in all_coins[:10]:
            clean_data.append({
                'name': coin['name'],
                'symbol': coin['symbol'],
                'price': float(coin['priceUsd']), # Стринг ирдэг тул тоо болгох
                'timestamp': full_data['timestamp']
            })
            
        return clean_data
        
    except Exception as e:
        print(f"API-тай холбогдоход алдаа гарлаа: {e}")
        return []

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram мэдэгдэл илгээхэд алдаа гарлаа: {e}")
    
