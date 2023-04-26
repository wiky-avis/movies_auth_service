import logging
from typing import Optional

from dotenv import load_dotenv
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import DecodeError, ExpiredSignatureError


load_dotenv()


logger = logging.getLogger(__name__)


def get_decoded_data(access_token: Optional[str]) -> Optional[dict]:
    if not access_token:
        return None

    try:
        decoded_token = decode_token(access_token)
    except (DecodeError, JWTDecodeError, ExpiredSignatureError):
        logger.error("Invalid token or expired signature.", exc_info=True)
        return
    return decoded_token
