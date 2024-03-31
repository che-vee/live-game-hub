import snowflake.connector
from task4_databases_init import get_snowflake_connection
from task4_redis_init import redis_client
import redis
import json
from bson import json_util
import time

def main():
    sf_conn = get_snowflake_connection()
    print('Snowflake connected.')

    try:
        print('Listening redis...')
        while True:
            data_to_pop = redis_client.rpop('sessions_list')

            if data_to_pop:
                session = json.loads(data_to_pop, object_hook=json_util.object_hook)
                print(session)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping the continuous pop operation.")
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")

    


# COPY INTO sf_sample.public.injestion_js ….. 

# insert into sf_sample.public.sample_js
# select current_timestamp(), 'mongoDB', Data from sf_sample.public.injestion_js;


# truncate sf_sample.public.injestion_js;

main()