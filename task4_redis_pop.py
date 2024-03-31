import snowflake.connector
from task4_databases_init import get_snowflake_connection
from task4_redis_init import redis_client
import redis
import json
from bson import json_util
import time
from bson import ObjectId
from datetime import datetime

def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()

def main():
    sf_conn = get_snowflake_connection()
    print('Snowflake connected.')

    try:
        redis_client.delete('sessions_list')
        print('Listening redis...')
        while True:
            data_to_pop = redis_client.rpop('sessions_list')

            if data_to_pop:
                sf_cur = sf_conn.cursor()
                session = json.loads(data_to_pop, object_hook=json_util.object_hook)
                session_json = json.dumps(session, default=custom_serializer)

                insert_query = """
                INSERT INTO INJESTION_SESSION (data) 
                SELECT PARSE_JSON(%s)
                """
                sf_cur.execute(insert_query, (session_json,))
                
                sf_cur.execute("""
                    INSERT INTO SAMPLE_SESSION 
                    SELECT current_timestamp(), 'mongoDB', data from INJESTION_SESSION
                    """
                ) 
                
                sf_cur.execute("TRUNCATE TABLE INJESTION_SESSION")
                sf_cur.close()

                print('pop success')

    except KeyboardInterrupt:
        print("Stopping the continuous pop operation.")
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")
    data_to_pop = redis_client.rpop('sessions_list')

main()