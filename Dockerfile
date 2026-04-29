FROM python:3.11-slim

WORKDIR /app

# Файлын нэрээ 's'-тэй эсэхийг заавал шалгаарай!
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Дата болон Лог хавтас үүсгэх
RUN mkdir -p data logs

# Питонд хаанаас ажиллуулахыг нь тодорхой зааж өгөх
CMD ["python", "main.py"]
