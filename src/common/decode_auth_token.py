import logging
from typing import Optional

import jwt
from flask import current_app


logger = logging.getLogger(__name__)


def get_user_id(token_header: Optional[str]) -> Optional[str]:
    if not token_header:
        return None

    try:
        decoded_token = jwt.decode(
            token_header,
            current_app.config.get("JWT_SECRET"),
            algorithms=[current_app.config.get("JWT_ALGORITHM")],
        )
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        logger.error("Invalid token or expired signature.", exc_info=True)
        return None
    return decoded_token.get("UserId")
