from http import HTTPStatus

from pyrate_limiter import Duration, Limiter, RedisBucket, RequestRate
from pyrate_limiter.exceptions import BucketFullException

from src.common.response import BaseResponse
from src.db.redis import redis_pool
from src.settings.config import RATELIMIT_ENABLED


rate_limits = (RequestRate(20, Duration.MINUTE),)

limiter = Limiter(
    *rate_limits,
    bucket_class=RedisBucket,
    bucket_kwargs={"redis_pool": redis_pool, "bucket_name": "auth"},
)


def allow_request(identity: str):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                if not RATELIMIT_ENABLED:
                    return result
                limiter.try_acquire(identity)
            except BucketFullException:
                return (
                    BaseResponse(
                        success=False, error={"msg": "Too Many Requests."}
                    ).dict(),
                    HTTPStatus.TOO_MANY_REQUESTS,
                )
            return result

        return wrapper

    return decorator_func
