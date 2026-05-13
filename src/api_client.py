import requests
import os
from dotenv import load_dotenv
import time
import telebot

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(token)
def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        raw_data = response.json()

        mapping = {
            'bitcoin': ('BTC', 'Bitcoin'),
            'ethereum': ('ETH', 'Ethereum'),
            'solana': ('SOL', 'Solana'),
            'binancecoin': ('BNB', 'BNB')
        }
        clean_data = []
        for coin_id, info in raw_data.items():
            symbol, name = mapping[coin_id]
            clean_data.append({
                'name': name,
                'symbol': symbol,
                'price': float(info['usd']),
                'timestamp': int(time.time() * 1000)
            })
        return clean_data
    except Exception as e:
        print(f"API Error (CoinGecko): {e}")
        return []

def send_telegram_alert(message):
    if not token or not chat_id:
        print("❌ Telegram Token эсвэл Chat ID олдсонгүй!")
        return
    try:
        bot.send_message(chat_id, message, parse_mode="Markdown")
    except Exception as e:
        print(f"❌ Telegram Connection Error: {e}")