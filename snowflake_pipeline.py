import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from game_hub.mongo_models import Viewer, ViewerPurchase
from app.snowflake_utils import get_snowflake_connection


def export_to_json(model, directory="/tmp"):
    filename = f"{model.__name__.lower()}_data.json"
    json_path = os.path.join(directory, filename)
    data = [document.to_mongo().to_dict() for document in model.objects]

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, default=str)
    return json_path



def create_table(table_name, schema_sql):
    conn = get_snowflake_connection()
    with conn.cursor() as cur:
        try:
            cur.execute(schema_sql)
            print(f"Verified: {table_name}")
        except Exception as e:
            print(f"Error in {table_name}: {e}")


def process_in_snowflake(
    json_path, ingestion_table, sample_table, model, stage_name="~"
):
    conn = get_snowflake_connection()
    with conn.cursor() as cur:
        cur.execute(f"PUT file://{json_path} @{stage_name}")
        cur.execute(
            f"COPY INTO {ingestion_table} FROM @{stage_name}/{os.path.basename(json_path)} FILE_FORMAT = (TYPE = 'JSON', STRIP_OUTER_ARRAY = TRUE)"
        )
        if model == Viewer:
            cur.execute(
                f"""
                INSERT INTO {sample_table} (processing_time, source_model, username, streamer_id, session_id, created_at, data)
                SELECT 
                    CURRENT_TIMESTAMP(), 
                    'mongodb', 
                    DATA:username::STRING, 
                    DATA:streamer_id::STRING, 
                    DATA:session_id::STRING, 
                    TO_TIMESTAMP_NTZ(DATA:created_at::STRING),
                    DATA VARIANT
                FROM {ingestion_table}
            """
            )
        elif model == ViewerPurchase:
            cur.execute(
                f"""
                INSERT INTO {sample_table} (processing_time, source_model, username, streamer_id, session_id, amount, currency, purchase_date, game_id, data)
                SELECT 
                    CURRENT_TIMESTAMP(), 
                    'mongodb', 
                    DATA:viewer_snapshot.username::STRING, 
                    DATA:viewer_snapshot.streamer_id::STRING,
                    DATA:viewer_snapshot.session_id::STRING,
                    DATA:amount::FLOAT, 
                    DATA:currency::STRING, 
                    TO_TIMESTAMP_NTZ(DATA:purchase_date::STRING),
                    DATA:game_id::STRING,
                    DATA VARIANT
                FROM {ingestion_table}
            """
            )

        cur.execute(f"TRUNCATE TABLE {ingestion_table}")

        file_name = os.path.basename(json_path)
        cur.execute(f"REMOVE @{stage_name}/{file_name}")


def main():
    model_sql = {
        Viewer: (
            "SF_SAMPLE.GAMINGPLATFORM.VIEWER",
            """
            CREATE TABLE IF NOT EXISTS SF_SAMPLE.GAMINGPLATFORM.VIEWER (
                PROCESSING_TIME DATETIME,
                SOURCE_MODEL VARCHAR(256),
                USERNAME VARCHAR(256),
                STREAMER_ID VARCHAR(256),
                SESSION_ID VARCHAR(256),
                CREATED_AT DATETIME,
                DATA VARIANT
            );
            """,
        ),
        ViewerPurchase: (
            "SF_SAMPLE.GAMINGPLATFORM.VIEWER_PURCHASE",
            """
            CREATE TABLE IF NOT EXISTS SF_SAMPLE.GAMINGPLATFORM.VIEWER_PURCHASE (
                PROCESSING_TIME DATETIME,
                SOURCE_MODEL VARCHAR(256),
                USERNAME VARCHAR(256),  
                STREAMER_ID VARCHAR(256),
                SESSION_ID VARCHAR(256),
                AMOUNT FLOAT, 
                CURRENCY VARCHAR(3),
                PURCHASE_DATE DATETIME,
                GAME_ID VARCHAR(256),
                DATA VARIANT 
            );
            """,
        ),
    }

    ingestion_table = "SF_SAMPLE.GAMINGPLATFORM.INJESTION_JS"
    ingestion_table_sql = """
        CREATE TABLE IF NOT EXISTS SF_SAMPLE.GAMINGPLATFORM.INJESTION_JS (
            DATA VARIANT
        );
    """

    for model, (sample_table, sample_table_sql) in model_sql.items():
        json_path = export_to_json(model)
        create_table(ingestion_table, ingestion_table_sql)
        create_table(sample_table, sample_table_sql)
        process_in_snowflake(json_path, ingestion_table, sample_table, model)


if __name__ == "__main__":
    main()
