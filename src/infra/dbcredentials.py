import boto3
import json
import os


def get_db_credentials():
    secret_name = os.environ["DB_SECRET_NAME"]
    region_name = os.environ["AWS_REGION"]

    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)
