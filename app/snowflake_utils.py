import os
import django
import snowflake.connector

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def get_snowflake_connection():
    return snowflake.connector.connect(
        user=settings.SNOWFLAKE_CONNECTION_PARAMS["user"],
        password=settings.SNOWFLAKE_CONNECTION_PARAMS["password"],
        account=settings.SNOWFLAKE_CONNECTION_PARAMS["account"],
        warehouse=settings.SNOWFLAKE_CONNECTION_PARAMS["warehouse"],
        database=settings.SNOWFLAKE_CONNECTION_PARAMS["database"],
        schema=settings.SNOWFLAKE_CONNECTION_PARAMS["schema"],
        ocsp_fail_open=False,
    )
