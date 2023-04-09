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

    def get_register_user_or_temporary_user(self, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        role = kwargs.get("role")
        self.repository.create_user(email=email, password=password)
        self.repository.create_role(email=email, role_name=role)
        user = self.repository.get_user(email=email)
        return UserResponse(
            id=user.id, email=user.email, roles=user.roles
        ).dict()
