import logging
from functools import wraps
from http import HTTPStatus
from typing import Any

from flask_restx import reqparse

from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse


logger = logging.getLogger(__name__)


def jwt_token_required() -> Any:
    def wrapper(fn):
        @wraps(fn)
        def decorator(request, *args, **kwargs):
            parser = reqparse.RequestParser()
            parser.add_argument("X-Auth-Token", location="headers")
            args = parser.parse_args()
            access_token = args.get("X-Auth-Token")
            auth_user_id = get_user_id(access_token)
            if not auth_user_id:
                logger.warning("Failed to get auth_user_id.")
                return (
                    BaseResponse(
                        success=False, error={"msg": "UndefinedUser."}
                    ).dict(),
                    HTTPStatus.UNAUTHORIZED,
                )
            return fn(request, *args, **kwargs)

        return decorator

    return wrapper
