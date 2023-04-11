import logging
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from src.api.v1.models.response import UserResponse
from src.common.response import BaseResponse
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def get_user_by_email(self, email: str):
        if not email:
            logger.error("Email is not valid: %s", email)
            return (
                BaseResponse(
                    success=False, error={"msg": "Email is not valid."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self.repository.get_user(email)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )
        user = UserResponse(id=str(user.id), email=user.email)
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

    def register_user(self, email: str, role: str) -> None:
        self.repository.create_user(email=email)
        user = self.repository.get_user(email)
        if not user:
            return
        self.repository.set_role(user, role)

    def get_user_roles(self, user_id: str) -> list:
        roles_ids = self.repository.get_ids_roles(user_id)
        roles = self.repository.get_roles(roles_ids)
        return roles

    def register_temporary_user(self, **kwargs):
        email = kwargs.get("email")
        role = RoleType.ROLE_TEMPORARY_USER.value

        try:
            self.register_user(email=email, role=role)
        except IntegrityError:
            logger.error(
                "User already exists: email %s.", email, exc_info=True
            )
            return (
                BaseResponse(
                    success=False, error={"msg": "User already exists."}
                ).dict(),
                HTTPStatus.CONFLICT,
            )

        user = self.repository.get_user(email)
        user_roles = self.get_user_roles(user.id)
        user = UserResponse(
            id=str(user.id),
            email=user.email,
            roles=user_roles,
            verified_mail=user.verified_mail,
            registered_on=str(user.registered_on),
        )
        return (
            BaseResponse(success=True, result=user).dict(),
            HTTPStatus.CREATED,
        )

    def get_list_user_login_history(self, user_id: str):
        login_history = self.repository.get_list_login_history(user_id)
        return (
            BaseResponse(success=True, result=login_history).dict(),
            HTTPStatus.OK,
        )
