import redis

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, socket_keepalive=True)
