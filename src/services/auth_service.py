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

    def register_user(self, email, role_name):
        self.repository.create_user(email=email)
        user = self.repository.get_user(email)
        if not user:
            return None
        self.repository.set_role(user, role_name)

    def get_user_roles(self, user_id):
        roles_ids = self.repository.get_ids_roles(user_id)
        roles = self.repository.get_roles(roles_ids)
        return roles

    def register_temporary_user(self, **kwargs):
        email = kwargs.get("email")
        role = kwargs.get("role")
        self.register_user(email, role)
        user = self.repository.get_user(email)
        user_roles = self.get_user_roles(user.id)
        print("---DATE", user.registered_on, type(user.registered_on))
        user = UserResponse(
            id=str(user.id),
            email=user.email,
            roles=user_roles,
            verified_mail=user.verified_mail,
            registered_on=user.registered_on,
        ).dict()
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK
