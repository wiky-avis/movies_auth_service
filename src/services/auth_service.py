import logging
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from src.api.v1.models.response import LoginHistoryResponse, UserResponse
from src.common.check_password import check_password
from src.common.pagination import get_pagination
from src.common.response import BaseResponse, Pagination
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
        user = self.repository.get_user_by_email(email)
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
        self.repository.create_user(email=email)
        user = self.repository.get_user_by_email(email=email)
        if not user:
            return
        self.repository.set_role(user, role)

    def approve_user(self, user_id: str, password: str):
        user = self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        if not password:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "Password is required."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        if user.verified_mail:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User already verified."},
                ).dict(),
                HTTPStatus.CONFLICT,
            )

        self.repository.set_role(
            user=user, role_name=RoleType.ROLE_PORTAL_USER.value
        )
        self.repository.set_password(user=user, password=password)
        self.repository.update_flag_verified_mail(user=user)

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
            HTTPStatus.OK,
        )

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

        user = self.repository.get_user_by_email(email=email)
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
        user = self.repository.get_user_by_id(user_id=user_id)
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
        self.repository.set_password(user, new_password)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def change_data(
        self,
        user_id: str,
        new_email: str | None,
    ):
        user = self.repository.get_user_by_id(user_id=user_id)
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

        user_by_email = self.repository.get_user_by_email(email=new_email)
        if user_by_email and (user_id != user_by_email.id):
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User with this email already exists."},
                ).dict(),
                HTTPStatus.CONFLICT,
            )
        self.repository.set_email(user, new_email)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def get_list_user_login_history(self, user_id: str, page, per_page):
        (
            login_history_data,
            login_history,
        ) = self.repository.get_list_login_history(user_id, page, per_page)
        pagination = Pagination(**get_pagination(login_history_data))
        return (
            LoginHistoryResponse(
                success=True, result=login_history, pagination=pagination
            ).dict(),
            HTTPStatus.OK,
        )
