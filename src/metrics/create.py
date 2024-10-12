import json
from datetime import date
from src.infra.dbconnect import get_db_connection


def handler(event, context):
    body = json.loads(event.get("body", {}))
    print(body)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO collected_health_metrics (timestamp, temperature, spo2, heart_rate, device_id) VALUES (%s, %s, %s, %s, %s)",
        (
            date.today(),
            body["temperature"],
            body["spo2"],
            body["heart_rate"],
            body["device_id"],
        ),
    )
    conn.commit()
    return {"statusCode": 200, "body": "Metric collected successfully"}
