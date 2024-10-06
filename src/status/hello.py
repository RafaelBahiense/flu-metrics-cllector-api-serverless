import psycopg2
import os
import json
from src.infra.dbcredentials import get_db_credentials


def handler(event, context):
    credentials = get_db_credentials()
    host = os.environ["DB_HOST"]
    port = 5432
    database = os.environ["DB_NAME"]
    user = credentials["username"]
    password = credentials["password"]

    try:
        conn = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()

        return {"statusCode": 200, "body": json.dumps({"db_version": db_version[0]})}
    except Exception as e:
        print(f"Database connection failed: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
