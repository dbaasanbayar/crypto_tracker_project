# 🚀 Crypto Live ETL Pipeline & AI Analyst

Энэхүү төсөл нь криптовалютын өгөгдлийг бодит хугацаанд (Real-time) татаж, **PostgreSQL** баазад хадгалан, **Llama 3.3 AI** загвар ашиглан зах зээлийн нэгтгэсэн шинжилгээ хийдэг, бүрэн автоматжуулсан **End-to-End Data Engineering** систем юм.

### 🔗 Live Links
* **Live Dashboard:** [Энд Railway-ийн линкээ тавиарай]
* **Telegram Bot:** `t.me/MyCryptoAlertBot` (Команд: `/latest_analysis`)

---

## 🛠 Технологийн стек (Tech Stack)

* **Language:** Python 3.11
* **Database:** Neon PostgreSQL (Serverless Storage)
* **AI Engine:** Groq Cloud - Llama 3.3 70B (Market Analysis)
* **Deployment:** Railway (CI/CD) & Docker
* **Data Visualization:** Streamlit & Plotly
* **Alerting:** Telegram Bot API (Custom Handlers & Threading)

---

## 🏗 Системийн архитектур (Architecture)

Систем нь **Decoupled Architecture** буюу өгөгдөл цуглуулах, боловсруулах, харуулах хэсгүүд нь бие даасан байдлаар зохион байгуулагдсан:

1.  **ETL Pipeline (Producer):** CoinGecko API-аас 30 минут тутамд өгөгдөл татаж, цэвэрлэн, PostgreSQL рүү хадгална.
2.  **Data Modeling (Fact/Dimension):** Өгөгдлийг **Star Schema** загвараар зохион байгуулсан нь аналитик хийх боломжийг оновчтой болгосон.
    * `assets` (Dimension Table): Зоосны ерөнхий мэдээлэл.
    * `price_history` (Fact Table): Үнийн түүхэн хөдөлгөөн болон цаг хугацааны тэмдэглэгээ.
3.  **AI Analysis (Llama 3.3):** 12 цаг тутамд баазаас сүүлийн өгөгдлийг шүүж, AI-аар зах зээлийн нэгтгэсэн дүгнэлт гаргуулна.
4.  **Monitoring & Alerting:** API тасрах эсвэл үнийн огцом хэлбэлзэл (>=1%) үед Telegram-аар шууд мэдээлнэ.



---

## 📊 Өгөгдлийн бүтэц (Data Schema)

Өгөгдлийн сангийн бүтэц нь аналитикчдад ашиглахад хялбар байхаар зохион байгуулагдсан:

| Хүснэгт | Төрөл | Тайлбар |
| :--- | :--- | :--- |
| `assets` | Dimension | `id`, `symbol`, `name` (Үндсэн мэдээлэл) |
| `price_history` | Fact | `asset_id`, `price`, `timestamp` (Түүхий өгөгдөл) |
| `hourly_summary` | Aggregated | `asset_id`, `avg_price`, `hour_timestamp` (Цаг тутмын нэгтгэл) |

---
📉 Системийн боломжууд
Interactive Analytics: Streamlit ашиглан түүхэн өгөгдлийг график хэлбэрээр харах.

AI Summary on Demand: Telegram бот дээр /latest_analysis команд өгч, AI-ийн хамгийн сүүлийн дүгнэлтийг шууд унших (Threading ашиглан бодит хугацаанд хариу өгнө).

Resilience: Алдааг хянах (Error handling) системтэй. API холболт тасарвал 3 цаг тутамд сануулга илгээнэ.

📈 Ирээдүйн сайжруулалтууд (Roadmap)
Phase 2: Great Expectations ашиглан өгөгдлийн чанарыг шалгах шүүлтүүр нэмэх.

Phase 2: GitHub Actions ашиглан автоматжуулсан CI/CD тохируулах.

Phase 3: Twitter эсвэл News API ашиглан Sentiment Analysis хийж, үнийн хөдөлгөөнтэй харьцуулах.