import boto3
import json
import os


def get_db_credentials():
    is_offline = os.environ.get("IS_OFFLINE", "false").lower() == "true"

    if is_offline:
        try:
            username = os.environ["DB_USER"]
            password = os.environ["DB_PASSWORD"]
            host = os.environ["DB_HOST"]
            port = os.environ.get("DB_PORT", "5432")
            database = os.environ["DB_NAME"]

            return {
                "username": username,
                "password": password,
                "host": host,
                "port": port,
                "database": database,
            }
        except KeyError as e:
            print(f"Missing environment variable: {e}")
            raise e
    else:
        secret_name = os.environ["DB_SECRET_NAME"]
        region_name = os.environ.get("AWS_REGION", "us-east-1")

        client = boto3.client("secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            raise e

        secret = get_secret_value_response["SecretString"]
        credentials = json.loads(secret)

        credentials["host"] = os.environ["DB_HOST"]
        credentials["port"] = os.environ.get("DB_PORT", "5432")
        credentials["database"] = os.environ["DB_NAME"]

        return credentials
