import os
import time

import jwt
from dotenv import load_dotenv

from src.config import TEST_PRIVATE_KEY


load_dotenv()


JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", default=600))
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", default=TEST_PRIVATE_KEY)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", default="RS256")


def generate_auth_token(expires_in=JWT_EXPIRES_IN, **kwargs):
    payload = {
        "user_id": kwargs.get("id"),
        "email": kwargs.get("email"),
        "verified_mail": kwargs.get("verified_mail"),
        "roles": kwargs.get("roles"),
        "exp": time.time() + expires_in,
    }
    token = jwt.encode(
        payload=payload,
        key=JWT_PRIVATE_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return token
