from datetime import date
from src.infra.dbconnect import get_db_connection


def handler(event, context):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO collected_health_metrics (timestamp, temperature, oxygen_saturation, pulse, device_id) VALUES (%s, %s, %s, %s, %s)",
        (
            date.today(),
            event["temperature"],
            event["oxygen_saturation"],
            event["pulse"],
            event["device_id"],
        ),
    )
    return {"statusCode": 200, "body": "Metric collected successfully"}
