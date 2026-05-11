import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def get_ai_analysis(coin_data):
    print(f"DEBUG: AI-руу явуулж буй датаны урт: {len(coin_data)}")
    if not coin_data:
        return "Дүн шинжилгээ хийх дата олдсонгүй."
    system_instruction = "Чи бол крипто арилжааны мэргэжлийн шинжээч. Хариуг үргэлж Монгол хэлээр, эможи ашиглаж, чухал тоонуудыг Bold болгоорой, Telegram-д тохиромжтой Markdown форматаар өгнө үү."
    
    user_prompt = f"Дараах дата дээр шинжилгээ хийж, зах зээлийн төлөв, эрсдэл, зөвлөмжийг гаргана уу:\n\n{coin_data}"
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[              
                {
                    "role": "system",
                    "content": system_instruction,
                },
                 {
                    "role": "user",
                    "content": user_prompt,
                }
            ]
        )
        print("DEBUG: Groq-оос амжилттай хариу авлаа.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: Groq-д гарсан алдаа: {e}")
        return f"AI Шинжилгээнд алдаа гарлаа: {str(e)}"
    