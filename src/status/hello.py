import json
from src.infra.dbconnect import get_db_connection


def handler(event, context):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()

        return {"statusCode": 200, "body": json.dumps({"db_version": db_version[0]})}
    except Exception as e:
        print(f"Database connection failed: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
