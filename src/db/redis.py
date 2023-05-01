import os

import redis
from dotenv import load_dotenv


load_dotenv()


redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST", default="redis"),
    port=int(os.getenv("REDIS_PORT", default=6379)),
    db=0,
)

redis_client = redis.StrictRedis(
    connection_pool=redis_pool,
    decode_responses=True,
)
