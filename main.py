from src.api_client import fetch_prices
from src.database import create_tables, save_to_db
import time

def run_pipeline():
    print("--- ETL Процесс эхэллээ ---")
    # 1. Хүснэгтүүдээ бэлдэх
    create_tables()
    
    while True:
        try: 
            print(f"\n[{time.strftime('%H:%M:%S')}] Дата татаж байна...")
            coins = fetch_prices()

            if coins:
                save_to_db(coins)
                print(f"Амжилттай: {len(coins)} зоосны дата хадгалагдлаа.")
            else:
                print("Анхаар: Дата олдсонгүй.")
        
        except Exception as e:
            print(f"Системд алдаа гарлаа: {e}")

        print("60 секунд хүлээнэ...")
        time.sleep(60)

if __name__ == "__main__":
    run_pipeline()

    