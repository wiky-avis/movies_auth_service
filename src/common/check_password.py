from werkzeug.security import check_password_hash


def check_password(password_hash, password):
    if not password:
        return False
    return check_password_hash(password_hash, password)
