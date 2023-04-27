from http import HTTPStatus

from src.app import jwt
from src.common.response import BaseResponse
from src.db.redis import redis_client


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload: dict):
    return (
        BaseResponse(
            success=False, error={"msg": "The token has been revoked."}
        ).dict(),
        HTTPStatus.NOT_FOUND,
    )
