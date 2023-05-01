from functools import wraps
from http import HTTPStatus

from werkzeug.exceptions import Unauthorized

from src import settings
from src.common.collections import get_in
from src.common.decode_auth_token import get_decoded_data
from src.common.response import BaseResponse
from src.db.db_models import RoleType


def admin_required(request):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            access_token = request.cookies.get("access_token_cookie")
            decoded_token = get_decoded_data(access_token)
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


def token_required(request, allowed_tokens):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get(settings.TOKEN_HEADER)
            if token not in allowed_tokens and settings.STRICT_TOKEN:
                raise Unauthorized("Token required")

            return fn(*args, **kwargs)

        return decorator

    return wrapper
