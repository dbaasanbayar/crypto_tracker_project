FROM python:3.11-slim
<<<<<<< HEAD
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . .
RUN mkdir -p data logs
CMD ["python", "main.py"]
=======

WORKDIR /app

# Файлын нэрээ 's'-тэй эсэхийг заавал шалгаарай!
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Дата болон Лог хавтас үүсгэх
RUN mkdir -p data logs

# Питонд хаанаас ажиллуулахыг нь тодорхой зааж өгөх
CMD ["python", "main.py"]
>>>>>>> 2c5a62abd813c2eb0b48428309ed2e455ce6c0e3
