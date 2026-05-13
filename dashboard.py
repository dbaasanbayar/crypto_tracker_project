import streamlit as st
import pandas as pd
import plotly.express as px
import time
from sqlalchemy import create_engine
import os

# 1. СЕТАП ХЭСЭГ (Хамгийн дээр байх ёстой)
st.set_page_config(page_title="Crypto Live Dashboard", layout="wide")

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return create_engine(db_url)

engine = get_engine()

# 2. ӨГӨГДӨЛ ТАТАХ ФУНКЦҮҮД (Дуудахаас өмнө тодорхойлсон байх)
def get_raw_data():
    """Сүүлийн үеийн түүхий өгөгдлийг татах"""
    query = """
    SELECT a.name, p.price, TO_TIMESTAMP(p.timestamp / 1000) as time
    FROM assets a
    JOIN price_history p ON a.id = p.asset_id
    ORDER BY p.timestamp DESC
    LIMIT 500
    """
    df = pd.read_sql_query(query, engine)
    return df

def get_hourly_data():
    """Нэгтгэсэн (Aggregated) өгөгдлийг татах"""
    query = """
    SELECT a.name, h.avg_price, h.hour_timestamp
    FROM assets a
    JOIN hourly_summary h ON a.id = h.asset_id
    ORDER BY h.hour_timestamp ASC
    """
    df = pd.read_sql_query(query, engine)
    return df

# 3. SIDEBAR (Тохиргоо)
st.sidebar.header("Тохиргоо")
auto_refresh = st.sidebar.checkbox("Автоматаар шинэчлэх", value=False)

# 4. ҮНДСЭН ХАРАГДАЦ (UI)
st.title("🚀 Crypto Live Monitor")
st.write("ETL системийн цуглуулсан өгөгдөл")

# --- RAW DATA SECTION ---
df = get_raw_data()

if not df.empty:
    st.subheader("💰 Хамгийн сүүлийн үеийн ханш")
    latest_df = df.groupby('name').first().reset_index()
    st.dataframe(latest_df, use_container_width=True)

    st.subheader("📈 Үнийн график (Сүүлийн өгөгдлүүд)")
    selected_coin = st.selectbox("Зоос сонгох:", df['name'].unique())
    filtered_df = df[df['name'] == selected_coin].sort_values('time')
    fig = px.line(filtered_df, x='time', y='price', title=f"{selected_coin} ханшийн хөдөлгөөн")
    st.plotly_chart(fig, use_container_width=True)

# --- HOURLY SUMMARY SECTION ---
st.subheader("📊 Цаг тутмын дундаж үнийн тренд")
df_hourly = get_hourly_data()

if not df_hourly.empty:
    fig_hourly = px.bar(df_hourly, x='hour_timestamp', y='avg_price', 
                        color='name', barmode='group',
                        title="Зоос бүрийн цаг тутмын дундаж үнэ")
    st.plotly_chart(fig_hourly, use_container_width=True)
else:
    st.info("Цаг тутмын нэгтгэсэн өгөгдөл хараахан цуглаагүй байна.")

# 5. CONTROL LOGIC (Хамгийн доор байх нь тохиромжтой)
if st.button('Шинэчлэх'):
    st.rerun()

if auto_refresh:
    time.sleep(60)
    st.rerun()

