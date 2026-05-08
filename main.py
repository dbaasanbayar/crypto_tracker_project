from src.api_client import fetch_prices, send_telegram_alert
from src.database import create_tables, save_to_db
from src.transform import aggregate_hourly_data
import time
import os

def run_pipeline():
    print("--- ETL Процесс эхэллээ ---")
    create_tables() # Хүснэгт бэлдэх
    
    last_prices = {} # Үнийн өөрчлөлт хянах санах ой
    last_agg_time = time.time() # Нэгтгэл хийсэн сүүлийн цаг
    
    while True:
        try:
            print(f"\n[{time.strftime('%H:%M:%S')}] Шинэ цикл эхэллээ...")
            
            # 1. Дата татах (Зөвхөн энд нэг удаа татна)
            coins = fetch_prices()
            
            # API-аас дата ирэхгүй бол (DNS эсвэл 403 алдаа)
            if not coins:
                error_msg = "⚠️ *ETL Alert:* API-аас дата ирсэнгүй. (DNS/Connection Error)"
                print(error_msg)
                
                # ТЕЛЕГРАМ РУУ МЭДЭГДЭХ
                send_telegram_alert(error_msg)
                
                print("600 секунд хүлээнэ...")
                time.sleep(600)
                continue

            # 2. Дата бааз руу хадгалах
            save_to_db(coins)
            print(f"✅ {len(coins)} зоосны дата хадгалагдлаа.")

            # 3. Үнийн өөрчлөлт болон Alert хянах
            for coin in coins:
                symbol = coin['symbol']
                current_price = coin['price']
                
                # Хуучин үнэ байгаа эсэхийг шалгах
                if symbol in last_prices:
                    old_price = last_prices[symbol]
                    change_pct = ((current_price - old_price) / old_price) * 100 

                    # 1%-иас их хэлбэлзэл гарвал мэдэгдэх
                    if abs(change_pct) >= 1.0:
                        direction = "🚀" if change_pct > 0 else "📉"
                        msg = f"{direction} *{symbol} Alert!*\nҮнэ: ${current_price:,.2f}\nӨөрчлөлт: {change_pct:+.2f}%"
                        send_telegram_alert(msg)
                
                # Одоогийн үнийг дараагийн циклд зориулж хадгалах
                last_prices[symbol] = current_price

            # 4. Цаг тутмын нэгтгэл (Aggregation) шалгах
            if time.time() - last_agg_time > 3600:
                print("--- Цаг тутмын нэгтгэл эхэлж байна ---")
                aggregate_hourly_data()
                last_agg_time = time.time()

        except Exception as e:
            err = f"🚨 *System Crash:* {str(e)}"
            print(err)
            send_telegram_alert(err)
            time.sleep(600)
        
        print("600 секунд хүлээнэ...")
        time.sleep(600)

if __name__ == "__main__":
    run_pipeline()