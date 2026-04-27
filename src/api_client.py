import requests

def fetch_prices():
    url = "https://api.coincap.io/v2/assets"
    
    # Мэргэжлийн түвшинд Header нэмэх (Optional but good)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
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

# Туршиж үзэх
if __name__ == "__main__":
    prices = fetch_prices()
    for p in prices:
        print(f"{p['name']} ({p['symbol']}): ${p['price']:.2f}")