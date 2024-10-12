import os
from alembic.config import Config
from alembic import command
from src.infra.dbcredentials import get_db_credentials


def run_migrations(event, context):
    credentials = get_db_credentials()
    db_url = f"postgresql+psycopg2://{credentials['username']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"

    alembic_ini_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../alembic.ini"
    )
    alembic_cfg = Config(alembic_ini_path)

    alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    script_location = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../alembic"
    )
    alembic_cfg.set_main_option("script_location", script_location)

    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully.")
        return {"statusCode": 200, "body": "Migrations applied successfully."}
    except Exception as e:
        print("Alembic Error:", str(e))
        return {"statusCode": 500, "body": f"Migration failed: {str(e)}"}
