import json
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
    columns = cur.description
    result = [
        {columns[index][0]: column for index, column in enumerate(value)}
        for value in cur.fetchall()
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, indent=4, sort_keys=True, default=str),
    }
