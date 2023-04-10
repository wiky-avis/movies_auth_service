import logging
from http import HTTPStatus

from src.api.v1.models.response import UserResponse
from src.common.response import BaseResponse
from src.repositories.auth_repository import AuthRepository


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def checking_mail(self, email):
        if not email:
            logger.error("Email is not valid: %s", email)
            return (
                BaseResponse(
                    success=False, error={"msg": "Email is not valid."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self.repository.find_by_email(email)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )
        result = UserResponse(id=str(user.id), email=user.email).dict()
        return BaseResponse(success=True, result=result).dict(), HTTPStatus.OK
