import os
from game_hub.mongo_models import Session
import django
import snowflake.connector
from django.conf import settings
from task4_databases_init import get_docs
from task4_redis_init import redis_client
import redis
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def main():
    data = get_docs()
    print('docs fetched.')

    try:
        is_ok = True
        redis_client.set('session_counter', 0)
        while is_ok:
            curr_id = redis_client.get('session_counter')
            curr_id = int(curr_id.decode())

            if data[curr_id] is not None:
                data_to_push = data[curr_id].to_json()
                redis_client.lpush('sessions_list', data_to_push)
            else:
                is_ok = False

            print(f'{curr_id}: push success.')
            
            redis_client.incr('session_counter')
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping the keep-alive connection.")
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")

main()
