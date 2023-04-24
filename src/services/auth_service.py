import logging
from http import HTTPStatus
from random import randint

from sqlalchemy.exc import IntegrityError

from src.api.v1.models.response import LoginHistoryResponse, UserResponse
from src.common.check_password import check_password
from src.common.pagination import get_pagination
from src.common.response import BaseResponse, Pagination
from src.db.db_models import RoleType
from src.db.redis import redis_client
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        roles_repository: RolesRepository,
    ):
        self.auth_repository = auth_repository
        self.roles_repository = roles_repository

    def get_user_by_email(self, email: str):
        if not email:
            logger.error("Email is not valid: %s", email, exc_info=True)
            return (
                BaseResponse(
                    success=False, error={"msg": "Email is not valid."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self.auth_repository.get_user_by_email(email)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )
        user_roles = self.get_user_roles(user.id)
        user = UserResponse(
            id=str(user.id),
            email=user.email,
            roles=user_roles,
            verified_mail=user.verified_mail,
            registered_on=str(user.registered_on),
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

    def register_user(self, email: str, role: str) -> None:
        self.auth_repository.create_user(email=email)
        user = self.auth_repository.get_user_by_email(email=email)
        if not user:
            return
        self.roles_repository.set_role_by_role_name(user, role)

    def get_user_roles(self, user_id: str) -> list:
        roles_ids = self.roles_repository.get_ids_roles_by_user_id(user_id)
        roles = self.roles_repository.get_role_names_by_ids(roles_ids)
        return roles

    def register_temporary_user(self, email: str, password: str):
        if not email or not password:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "No email or no password."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        role = RoleType.ROLE_PORTAL_USER.value
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

        user = self.auth_repository.get_user_by_email(email=email)
        self.auth_repository.set_password(user=user, password=password)
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

    def change_password(
        self,
        user_id: str,
        old_password: str | None,
        new_password: str | None,
    ):
        user = self.auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        if not new_password or not old_password:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "No new password or no old password."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        check_old_password = check_password(user.password_hash, old_password)
        if not check_old_password:
            return (
                BaseResponse(
                    success=False, error={"msg": "Invalid password."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )
        self.auth_repository.set_password(user, new_password)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def change_data(
        self,
        user_id: str,
        new_email: str | None,
    ):
        user = self.auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        if not new_email:
            return (
                BaseResponse(
                    success=False, error={"msg": "No new email."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        user_by_email = self.auth_repository.get_user_by_email(email=new_email)
        if user_by_email and (user_id != user_by_email.id):
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User with this email already exists."},
                ).dict(),
                HTTPStatus.CONFLICT,
            )
        self.auth_repository.set_email(user, new_email)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def get_list_user_login_history(self, user_id: str, page, per_page):
        (
            login_history_data,
            login_history,
        ) = self.auth_repository.get_list_login_history(
            user_id, page, per_page
        )
        pagination = Pagination(**get_pagination(login_history_data))
        return (
            LoginHistoryResponse(
                success=True, result=login_history, pagination=pagination
            ).dict(),
            HTTPStatus.OK,
        )

    def delete_account(self, user_id: str):
        user = self.auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User not found."},
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self.auth_repository.delete_user(user=user)
        return (
            BaseResponse(success=True).dict(),
            HTTPStatus.NO_CONTENT,
        )

    def email_confirmation(self, secret_code: str, user_id: str):
        code_in_redis = redis_client.get(user_id)
        if code_in_redis and secret_code == code_in_redis:
            user = self.auth_repository.get_user_by_id(user_id=user_id)
            self.auth_repository.update_flag_verified_mail(user=user)
            return (
                BaseResponse(success=True, result="Ok").dict(),
                HTTPStatus.OK,
            )
        return BaseResponse(success=False).dict(), HTTPStatus.NOT_FOUND

    def send_code(self, user_id: str):
        user = self.auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User not found."},
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        redis_client.set(user_id, randint(10000, 99999), 900)
        # TODO: Отправка кода подтверждения на почту
        # send_code_to_email(
        #     app=current_app,
        #     body=redis_client.get(user_id),
        #     recipients=[user.email]
        # )

        return (
            BaseResponse(success=True, result="Ok").dict(),
            HTTPStatus.OK,
        )
