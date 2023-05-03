from werkzeug.security import check_password_hash

from src.common.tracer import trace_request as trace


@trace("check_password")
def check_password(password_hash, password):
    if not password:
        return False
    return check_password_hash(password_hash, password)
