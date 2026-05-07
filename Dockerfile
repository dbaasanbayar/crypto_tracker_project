FROM python:3.11-slim

# Системийн сангуудыг суулгах (psycopg2-т хэрэгтэй)
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Buffer-ийг унтрааснаар Railway-ийн Logs дээр бичиг шууд харагдана
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]