import requests
import os
from dotenv import load_dotenv
import time

# 1. .env файлыг уншиж эхлүүлэх
load_dotenv()
# 2. Түлхүүрийг орчны хувьсагчаас татаж авах
# Хэрэв олдохгүй бол None буцаана
COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")

def fetch_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]
    # Түлхүүр байхгүй бол анхааруулга өгөх
    
    try: 
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Хэрэв 404 эсвэл 500 алдаа гарвал шууд except рүү үсрэнэ
        
        full_data = response.json() # Бүх датаг авах
        
        clean_data = []
        # Зөвхөн эхний 10 зоосыг туршилтаар авъя
        for item in full_data:
            if item['symbol'] in symbols:
                clean_data.append({
                    'name': item['symbol'].replace("USDT", ""),
                    'symbol': item['symbol'],
                    'price': float(item['price']),
                    'timestamp': int(time.time() * 1000)
                })
        return clean_data
    except Exception as e:
        print(f"API Error: {e}")
        return []

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Telegram Token эсвэл Chat ID олдсонгүй!")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            print(f"❌ Telegram Error: {r.status_code}, {r.text}")
    except Exception as e:
        print(f"❌ Telegram Connection Error: {e}")