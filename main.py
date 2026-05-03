from src.api_client import fetch_prices, send_telegram_alert
from src.database import create_tables, save_to_db
import time
from src.transform import aggregate_hourly_data

last_prices = {}

def run_pipeline():
    print("--- ETL Процесс эхэллээ ---")
    # 1. Хүснэгтүүдээ бэлдэх
    create_tables()
    
    # 1. Давталт эхлэхээс өмнө хугацааг тэмдэглэж авна
    aggregate_hourly_data()
    last_agg_time = time.time()
    
    while True:
        try: 
            print(f"\n[{time.strftime('%H:%M:%S')}] Дата татаж байна...")
            coins = fetch_prices()

            # 2. Нэгтгэл хийх нөхцөл
            if time.time() - last_agg_time > 3600:
                print("--- Цаг тутмын нэгтгэл эхэлж байна ---")
                aggregate_hourly_data()
                last_agg_time = time.time()

            if coins:
                save_to_db(coins)
                print(f"Амжилттай: {len(coins)} зоосны дата хадгалагдлаа.")
                for coin in coins:
                    symbol = coin['symbol']
                    current_price = coin['price']
                    
                    # 1. Эхлээд харьцуулалт хийх (Хуучин үнэ байгаа эсэхийг шалгах)
                    if symbol in last_prices:
                        old_price = last_prices[symbol]
                        change_pct = ((current_price - old_price) / old_price) * 100 

                        if abs(change_pct) >= 1.0:
                            msg = f"🚀 *{symbol} Alert!*\nҮнэ: ${current_price:,.2f}\nӨөрчлөлт: {change_pct:+.2f}%"
                            send_telegram_alert(msg)
                    
                    # 2. ХАРЬЦУУЛЖ ДУУССАНЫ ДАРАА шинэ үнийг хадгалах
                    # Ингэснээр дараагийн 60 секундэд энэ үнэ 'old_price' болж ашиглагдана.
                    last_prices[symbol] = current_price

        except Exception as e:
            print(f"Системд алдаа гарлаа: {e}")
        print("60 секунд хүлээнэ...")
        time.sleep(60)

if __name__ == "__main__":
    run_pipeline()
