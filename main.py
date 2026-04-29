from src.api_client import fetch_prices
from src.database import create_tables, save_to_db

def run_pipeline():
    print("--- ETL Процесс эхэллээ ---")
    
    # 1. Хүснэгтүүдээ бэлдэх
    create_tables()
    
    # 2. Датагаа татаж авах
    coins = fetch_prices()
    
    if coins:
        # 3. Датагаа өгөгдлийн санд хадгалах
        save_to_db(coins)
        print(f"Амжилттай: {len(coins)} зоосны датаг боловсрууллаа.")
    else:
        print("Дата олдсонгүй.")

if __name__ == "__main__":
    run_pipeline()