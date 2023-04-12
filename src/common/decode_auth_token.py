import logging
import os
from typing import Optional

import jwt

from src.config import TEST_PUBLIC_KEY


logger = logging.getLogger(__name__)


JWT_SECRET = TEST_PUBLIC_KEY
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_user_id(token_header: Optional[str]) -> Optional[str]:
    if not token_header:
        return None

    try:
        decoded_token = jwt.decode(
            token_header,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        logger.error("Invalid token or expired signature.", exc_info=True)
        return None
    return decoded_token.get("UserId")
