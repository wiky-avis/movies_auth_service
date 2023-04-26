from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import DecodeError

from src.common.collections import get_in
from src.common.response import BaseResponse
from src.db.db_models import RoleType


def admin_required(request):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            access_token = request.cookies.get("access_token_cookie")
            try:
                decoded_token = decode_token(access_token)
            except (DecodeError, JWTDecodeError):
                decoded_token = None
            roles = get_in(decoded_token, "sub", "roles")
            if RoleType.ROLE_PORTAL_ADMIN not in roles:
                return (
                    BaseResponse(
                        success=False, error={"msg": "Forbidden. Admins only."}
                    ).dict(),
                    HTTPStatus.FORBIDDEN,
                )
            return fn(*args, **kwargs)

        return decorator

    return wrapper
