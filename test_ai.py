from src.database import get_recent_prices
from src.ai_analyzer import get_ai_analysis

# 1. Баазаас дата ирж байгааг шалгах
data = get_recent_prices(5)
print("--- DATABASE DATA ---")
print(data)

if not data:
    print("❌ АЛДАА: Баазаас дата ирсэнгүй!")
else:
    # 2. AI-аас хариу ирж байгааг шалгах
    print("\n--- AI RESPONSE ---")
    result = get_ai_analysis(data)
    print(result)