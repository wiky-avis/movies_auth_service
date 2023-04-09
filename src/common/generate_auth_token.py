import time

import jwt
from flask import current_app


def generate_auth_token(
    expires_in=current_app.config.get("JWT_EXPIRES_IN"), **kwargs
):
    payload = {
        "UserId": kwargs.get("id"),
        "Email": kwargs.get("email"),
        "VerifiedMail": kwargs.get("verified_mail"),
        "Roles": kwargs.get("roles"),
        "exp": time.time() + expires_in,
    }
    token = jwt.encode(
        payload,
        current_app.config.get("JWT_PRIVATE_KEY"),
        algorithm=current_app.config.get("JWT_ALGORITHM"),
    )
    return token
