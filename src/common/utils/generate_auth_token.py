import time

import jwt

from src.app import app


def generate_auth_token(expires_in=app.config["JWT_EXPIRES_IN"], **kwargs):
    payload = {
        "UserId": kwargs.get("id"),
        "Email": kwargs.get("email"),
        "VerifiedMail": kwargs.get("verified_mail"),
        "Roles": kwargs.get("roles"),
        "exp": time.time() + expires_in,
    }
    token = jwt.encode(
        payload,
        app.config["JWT_PRIVATE_KEY"],
        algorithm=app.config["JWT_ALGORITHM"],
    )
    return token
