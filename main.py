from src.api_client import fetch_prices, send_telegram_alert
from src.database import create_tables, save_to_db
from src.transform import aggregate_hourly_data
from src.ai_analyzer import get_ai_analysis  # Шинэ AI функц
from src.database import get_recent_prices  # Баазаас дата унших функц
import time

def run_pipeline():
    print("--- ETL Процесс эхэллээ ---")
    create_tables() 
    
    last_prices = {} # Үнийн өөрчлөлт хянах санах ой
    last_agg_time = time.time() # Нэгтгэл хийсэн сүүлийн цаг
    last_err_time = 0

    FETCH_INTERVAL = 30 * 60
    ALERT_INTERVAL = 3 * 60 * 60
    AI_AGG_INTERVAL = 60

    while True:
        try:
            print(f"\n[{time.strftime('%H:%M:%S')}] Шинэ цикл эхэллээ...")
            coins = fetch_prices()
            
            if not coins:
                if time.time() - last_err_time > ALERT_INTERVAL:
                    send_telegram_alert("⚠️ *System Alert:* API холболт тасарлаа. (3 цаг тутамд сануулж байна)")
                    last_error_time = time.time()
                
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
                    print("--- 6 цагийн AI Шинжилгээ эхэллээ ---")
                    aggregate_hourly_data()

                    recent_data = get_recent_prices()
                    ai_conclusion = get_ai_analysis(recent_data)
                    print(ai_conclusion)
                    send_telegram_alert(f"🤖 *6-Hour Market Report (Llama 3):*\n\n{ai_conclusion}")
                    last_agg_time = time.time()
            
        except Exception as e:
            print(f"🚨 Алдаа: {e}")
            send_telegram_alert(f"🚨 *Critical Crash:* {str(e)[:100]}")
            time.sleep(FETCH_INTERVAL)
        
        print("✅ Цикл дууслаа. 30 минут хүлээнэ...")
        time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    run_pipeline()


