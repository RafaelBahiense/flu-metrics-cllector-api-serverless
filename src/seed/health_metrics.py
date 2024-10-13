import random
from datetime import datetime, timedelta
from psycopg2.extras import execute_values
from src.infra.dbconnect import get_db_connection

def generate_random_data(device_id, num_days=30):
    data = []
    for i in range(num_days):
        timestamp = datetime.now() - timedelta(days=i)
        temperature = round(random.uniform(36.5, 39.5), 1)
        spo2 = round(random.uniform(90.0, 99.0), 1)
        heart_rate = random.randint(60, 100)
        
        data.append((
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            temperature,
            spo2,
            heart_rate,
            device_id
        ))
    
    return data

def handler(event, context):
    device_id = "device124443"
    num_days = 30

    health_metrics = generate_random_data(device_id, num_days)
    print(f"Generated {len(health_metrics)} records")

    conn = get_db_connection()
    cur = conn.cursor()

    insert_query = """
        INSERT INTO collected_health_metrics (timestamp, temperature, spo2, heart_rate, device_id)
        VALUES %s
    """

    try:
        execute_values(cur, insert_query, health_metrics)
        conn.commit()
        print(f"Successfully inserted {len(health_metrics)} rows.")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return {
        "statusCode": 200,
        "body": f"Seeded {len(health_metrics)} records into the database."
    }