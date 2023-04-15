import os

import redis
from dotenv import load_dotenv


load_dotenv()


redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", default="redis"),
    port=int(os.getenv("REDIS_PORT", default=6379)),
    db=0,
    decode_responses=True,
)
