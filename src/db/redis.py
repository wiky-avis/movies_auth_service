import os

import redis


redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0,
    decode_responses=True,
)
