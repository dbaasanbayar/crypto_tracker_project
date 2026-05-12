from src.database import get_connection

def aggregate_hourly_data():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO hourly_summary (
        asset_id,
        avg_price,
        max_price,
        min_price,
        hour_timestamp
    )
    SELECT 
        asset_id,
        AVG(price),
        MAX(price),
        MIN(price),
        DATE_TRUNC('hour', TO_TIMESTAMP(timestamp / 1000)) as hour
    FROM price_history
    WHERE timestamp >= (EXTRACT(EPOCH FROM NOW()) - 3600) * 1000
    GROUP BY asset_id, hour
    ON CONFLICT DO NOTHING;
"""

    try: 
        cursor.execute(query)
        conn.commit()
        print("✅ Hourly aggregation амжилттай хийгдлээ.")
    except Exception as e:
        print(f"❌ Aggregation алдаа: {e}")
    finally:
        conn.close()