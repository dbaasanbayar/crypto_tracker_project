import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px # График зурахад ашиглана

# Хуудасны тохиргоо
st.set_page_config(page_title="Crypto Live Dashboard", layout="wide")

def get_data():
    conn = sqlite3.connect('data/crypto.db')
    # Сүүлийн 100 бичлэгийг татаж авах SQL
    query = """
    SELECT a.name, p.price, datetime(p.timestamp/1000, 'unixepoch') as time
    FROM assets a
    JOIN price_history p ON a.id = p.asset_id
    ORDER BY p.timestamp DESC
    LIMIT 500
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🚀 Crypto Live Monitor")
st.write("ETL системийн цуглуулсан өгөгдөл")

# Датагаа татаж авах
df = get_data()

if not df.empty:
    # 1. Сүүлийн үеийн үнийн хүснэгт
    st.subheader("💰 Хамгийн сүүлийн үеийн ханш")
    latest_df = df.groupby('name').first().reset_index()
    st.dataframe(latest_df, use_container_width=True)

    # 2. Үнийн өөрчлөлтийн график
    st.subheader("📈 Үнийн график (Сүүлийн өгөгдлүүд)")
    selected_coin = st.selectbox("Зоос сонгох:", df['name'].unique())
    
    filtered_df = df[df['name'] == selected_coin].sort_values('time')
    
    fig = px.line(filtered_df, x='time', y='price', title=f"{selected_coin} ханшийн хөдөлгөөн")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Өгөгдлийн санд дата олдсонгүй.")

# Dashboard-ийн нэмэлт функц
st.sidebar.header("Тохиргоо")
auto_refresh = st.sidebar.checkbox("Автоматаар шинэчлэх", value=False)

if auto_refresh:
    import time
    time.sleep(60) # 60 секунд тутамд
    st.rerun()    # Хуудсыг автоматаар дахин ачаална

# 60 секунд тутамд хуудсыг шинэчлэх товч
if st.button('Шинэчлэх'):
    st.rerun()
