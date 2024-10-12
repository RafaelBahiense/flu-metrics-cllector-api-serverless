from src.infra.dbconnect import get_db_connection


def handler(event, context):
    conn = get_db_connection()
    cur = conn.cursor()

    if "limit" not in event:
        event["limit"] = 10
    if "page" not in event:
        event["page"] = 1

    event["offset"] = (event["page"] - 1) * event["limit"]

    cur.execute(
        "SELECT * FROM collected_health_metrics ORDER BY timestamp DESC LIMIT (%s) OFFSET (%s)",
        (event["limit"], event["offset"]),
    )
    metrics = cur.fetchall()
    return {"statusCode": 200, "body": str(metrics)}
