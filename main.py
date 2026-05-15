from src.api_client import fetch_prices, send_telegram_alert, bot
from src.database import create_tables, save_to_db
from src.transform import aggregate_hourly_data
from src.ai_analyzer import get_ai_analysis  # Шинэ AI функц
from src.database import get_recent_prices  # Баазаас дата унших функц
import time
import threading

latest_report = "Хүлээж байна..."
# 1. Telegram командын хэсэг (Циклийн гадна байх ёстой)
@bot.message_handler(commands=['start', 'help'])

def send_welcome(message):
    welcome_text = (
        "👋 *Сайн байна уу! Би Баасанбаярын AI Шинжээч байна.*\n\n"
        "📈 Би 30 минут тутамд крипто үнэ цуглуулж, 12 цаг тутамд "
        "Llama 3.3 ашиглан зах зээлийн нэгтгэсэн тайлан гаргадаг.\n\n"
        "👉 /latest_analysis - Сүүлийн тайланг унших"
    )
    bot.reply_to(message, welcome_text, parse_mode='HTML')
    
@bot.message_handler(commands=['latest_analysis'])
def send_latest(message):
    global latest_report
    response = f"📊 *Сүүлийн 12 цагийн нэгтгэсэн тайлан:* \n\n{latest_report}"
    bot.reply_to(message, response, parse_mode='HTML')
    
def run_bot():
    print("🤖 Telegram Bot команд сонсож эхэллээ...")
    bot.infinity_polling()
    
def run_pipeline():
    global latest_report
    print("--- ETL Процесс эхэллээ ---")
    create_tables() 
    
    last_prices = {} # Үнийн өөрчлөлт хянах санах ой
    last_agg_time = time.time() # Нэгтгэл хийсэн сүүлийн цаг
    last_err_time = 0

    FETCH_INTERVAL = 30 * 60
    ALERT_INTERVAL = 3 * 60 * 60
    AI_AGG_INTERVAL = 12 * 60 * 60

    latest_report = "Одоогоор тайлан бэлэн болоогүй байна. 12 цагийн циклийг хүлээнэ үү."

    while True:
        try:
            print(f"\n[{time.strftime('%H:%M:%S')}] Шинэ цикл эхэллээ...")
            coins = fetch_prices()
            
            if not coins:
                if time.time() - last_err_time > ALERT_INTERVAL:
                    send_telegram_alert("⚠️ *System Alert:* API холболт тасарлаа. (3 цаг тутамд сануулж байна)")
                    last_err_time = time.time()
                
                print(f"Дараагийн оролдлого 30 минутын дараа...")
                time.sleep(FETCH_INTERVAL)
                continue
                
            # 2. Дата бааз руу хадгалах
            save_to_db(coins)

            # 3. Үнийн өөрчлөлт болон Alert хянах
            for coin in coins:
                symbol = coin['symbol']
                price = coin['price']
                if symbol in last_prices:
                    change_pct = ((price - last_prices[symbol]) / last_prices[symbol]) * 100
                    if abs(change_pct) >= 1.0:
                        send_telegram_alert(f"{'🚀' if change_pct > 0 else '📉'} *{symbol}* үнэ: ${price:,.2f} ({change_pct:+.2f}%)")
                last_prices[symbol] = price

            # 4. Цаг тутмын нэгтгэл (Aggregation) шалгах
            if time.time() - last_agg_time > AI_AGG_INTERVAL:
                    print("--- 12 цагийн AI Шинжилгээ эхэллээ ---")
                    aggregate_hourly_data()
                    recent_data = get_recent_prices(24)

                    ai_conclusion = get_ai_analysis(recent_data)
                    latest_report = ai_conclusion
    
                    send_telegram_alert(f"🤖 *12-Hour Market Report (Llama 3):*\n\n{ai_conclusion}")
                    last_agg_time = time.time()
                    
        except Exception as e:
            print(f"🚨 Алдаа: {e}")
            send_telegram_alert(f"🚨 *Critical Crash:* {str(e)[:100]}")
            time.sleep(FETCH_INTERVAL)
        
        print("✅ Цикл дууслаа. 30 минут хүлээнэ...")
        time.sleep(FETCH_INTERVAL)
        
if __name__ == "__main__":
    # 3. Бот болон ETL-ийг зэрэг ажиллуулах (Threading)
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    run_pipeline()




