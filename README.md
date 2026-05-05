# 🚀 Crypto Live ETL Pipeline & Dashboard

Энэхүү төсөл нь криптовалютын ханшийг бодит хугацаанд (Real-time) татаж, боловсруулан, хянах боломжтой бүрэн автоматжуулсан **Data Engineering** систем юм. Docker орчинд ажиллах ба Python, SQLite, болон Streamlit технологиудыг ашигласан.



## 🛠 Технологийн стек (Tech Stack)

*   **Language:** Python 3.11
*   **Containerization:** Docker & Docker Compose
*   **Database:** SQLite (Persistent storage via Docker Volumes)
*   **Data Visualization:** Streamlit & Plotly
*   **Alerting:** Telegram Bot API
*   **Libraries:** Pandas, Requests, Schedule

## 🏗 Системийн архитектур (Architecture)

Систем нь дараах 3 үндсэн хэсгээс бүрдэнэ:

1.  **ETL Pipeline (Producer):** CoinGecko API-аас минут тутамд өгөгдөл татаж, цэвэрлэн, SQLite бааз руу хадгална. Үнийн огцом өөрчлөлтийг Telegram-аар мэдээлнэ.
2.  **Data Transformation:** Цаг тутамд түүхий өгөгдлийг нэгтгэж (Aggregation), аналитик хийхэд бэлэн болгон `hourly_summary` хүснэгтэд хадгална.
3.  **Analytics Dashboard (Consumer):** Хадгалагдсан өгөгдлийг интерактив график хэлбэрээр хэрэглэгчид харуулна.

## 🚀 Хэрхэн ажиллуулах вэ?

### 1. Урьдчилсан нөхцөл
*   Mac эсвэл Windows дээр **Docker Desktop** суусан байх.
*   `.env` файл үүсгэж Telegram ботын мэдээллээ оруулсан байх.

### 2. Ажиллуулах тушаал
Төслийн хавтас дотор терминалаа нээгээд дараах тушаалыг өгнө:
```bash
docker-compose up -d --build

### 3. Dashboard нээх
Контейнерууд амжилттай ассаны дараа чи өөрийн дуртай вэб хөтөч (Chrome, Safari г.м) дээр дараах хаягийг нээж, бодит хугацааны аналитикийг харах боломжтой:

🔗 **URL:** [http://localhost:8501](http://localhost:8501)

*Тэмдэглэл: Хэрэв чи Docker-ийг үүлэн сервер дээр ажиллуулж байгаа бол `localhost`-ийн оронд тухайн серверийн IP хаягийг ашиглана уу.*

### 4. 📊 Өгөгдлийн бүтэц (Data Schema)

Өгөгдлийн сангийн бүтэц нь Relational загвартай бөгөөд дата саянтист болон аналитикчдад ашиглахад хялбар байхаар зохион байгуулагдсан:

assets хүснэгт: Системийн хянаж буй криптовалютуудын үндсэн мэдээлэл.

* id: Primary Key.

* symbol: Зоосны тэмдэг (жишээ нь: btc).

* name: Зоосны нэр (жишээ нь: Bitcoin).

price_history хүснэгт: Минут тутамд татаж авсан түүхий өгөгдөл (Raw data).

* asset_id: assets хүснэгттэй холбогдох     Foreign Key.

* price: Тухайн үеийн ханш (USD).

* timestamp: Өгөгдөл татсан цаг хугацаа (Unix format).

hourly_summary хүснэгт: Аналитик хийхэд зориулсан нэгтгэсэн өгөгдөл (Aggregated data).

* asset_id: Foreign Key.

* avg_price: Тухайн цаг дахь дундаж үнэ.

* hour_timestamp: Цаг тутмын тэмдэглэгээ.


### 5. 📈 Ирээдүйн сайжруулалтууд (Roadmap)


Энэхүү төсөл нь цаашид илүү мэргэжлийн түвшний Data Engineering Platform болон өргөжих бүрэн боломжтой:

Data Quality & Validation (Phase 2):

Great Expectations эсвэл Pydantic ашиглан өгөгдлийн чанарыг шалгах шүүлтүүр нэмэх.

Буруу эсвэл дутуу дата орж ирэх үед ажиллах "Error Handling" логикийг сайжруулах.

Cloud Deployment & CI/CD (Phase 2):

Системийг AWS эсвэл Google Cloud дээр байршуулж, 24/7 тасралтгүй ажиллуулах.

GitHub Actions ашиглан автоматжуулсан тест болон deployment (CI/CD) тохируулах.

Data Enrichment & AI (Phase 3):

Крипто мэдээ болон сошиал медиагийн хандлагыг (Sentiment Analysis) татаж, үнийн хөдөлгөөнтэй харьцуулах.

Түүхэн өгөгдөл дээр суурилсан Machine Learning модел ашиглан үнийн таамаглал хийх хэсэг нэмэх.