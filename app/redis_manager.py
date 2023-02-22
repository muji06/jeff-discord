import redis

class RedisManager(object):
    def __init__(self):
        conn = redis.Redis(host="redis_jeff",port=6379, db=1)
        self.cache = conn

cache = RedisManager()
