import psycopg2
from src.infra.dbcredentials import get_db_credentials
from psycopg2._psycopg import connection


def get_db_connection() -> connection:
    db_credentials = get_db_credentials()
    host = db_credentials["host"]
    port = db_credentials["port"]
    database = db_credentials["database"]
    user = db_credentials["username"]
    password = db_credentials["password"]
    return psycopg2.connect(
        host=host, port=port, database=database, user=user, password=password
    )
