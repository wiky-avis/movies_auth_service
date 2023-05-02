import logging
from http import HTTPStatus
from random import randint
from typing import NoReturn

from flask import current_app, make_response, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from user_agents import parse

from src.api.base.models.login_history import LoginHistoryResponse
from src.api.base.models.user import UserResponse
from src.common.check_device import check_device_type
from src.common.check_password import check_password
from src.common.pagination import get_pagination
from src.common.response import BaseResponse, Pagination
from src.common.send_email import send_to_email
from src.common.tracer import trace_request as trace
from src.db.db_models import ActionType, RoleType
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
        self._auth_repository = auth_repository
        self._roles_repository = roles_repository

    def create_admin(self, email: str, password: str) -> NoReturn:
        user = self._auth_repository.get_user_by_email(email)
        if user:
            raise MultipleResultsFound

        self._auth_repository.create_admin(email=email, password=password)
        admin_user = self._auth_repository.get_user_by_email(email=email)
        self._roles_repository.set_role_by_role_name(
            user=admin_user, role_name=RoleType.ROLE_PORTAL_ADMIN.value
        )

    def get_user_by_email(self, email: str):
        if not email:
            logger.error("Email is not valid: %s", email, exc_info=True)
            return (
                BaseResponse(
                    success=False, error={"msg": "Email is not valid."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self._auth_repository.get_user_by_email(email)
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

    def register_user(self, email: str, role: str) -> NoReturn:
        self._auth_repository.create_user(email=email)
        user = self._auth_repository.get_user_by_email(email=email)
        if not user:
            return
        self._roles_repository.set_role_by_role_name(user, role)

    @trace("get_user_roles")
    def get_user_roles(self, user_id: str) -> list:
        roles_ids = self._roles_repository.get_ids_roles_by_user_id(user_id)
        roles = self._roles_repository.get_role_names_by_ids(roles_ids)
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

        user = self._auth_repository.get_user_by_email(email=email)
        self._auth_repository.set_password(user=user, password=password)
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
        old_password: str,
        new_password: str,
    ):
        user = self._auth_repository.get_user_by_id(user_id=user_id)
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
        self._auth_repository.set_password(user, new_password)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def change_data(self, user_id: str, new_email: str):
        user = self._auth_repository.get_user_by_id(user_id=user_id)
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

        user_by_email = self._auth_repository.get_user_by_email(
            email=new_email
        )
        if user_by_email and (user_id != user_by_email.id):
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User with this email already exists."},
                ).dict(),
                HTTPStatus.CONFLICT,
            )
        self._auth_repository.set_email(user, new_email)

        return BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK

    def get_list_user_login_history(
        self, user_id: str, page: int, per_page: int
    ):
        (
            login_history_data,
            login_history,
        ) = self._auth_repository.get_list_login_history(
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
        user = self._auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User not found."},
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self._auth_repository.delete_user(user=user)
        return (
            BaseResponse(success=True).dict(),
            HTTPStatus.NO_CONTENT,
        )

    def email_confirmation(self, secret_code: str, user_id: str):
        code_in_redis = redis_client.get(user_id)
        if code_in_redis and secret_code == code_in_redis:
            user = self._auth_repository.get_user_by_id(user_id=user_id)
            self._auth_repository.update_flag_verified_mail(user=user)
            return (
                BaseResponse(success=True, result="Ok").dict(),
                HTTPStatus.OK,
            )
        return BaseResponse(success=False).dict(), HTTPStatus.NOT_FOUND

    def send_code(self, user_id: str):
        user = self._auth_repository.get_user_by_id(user_id=user_id)
        if not user:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "User not found."},
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        redis_client.set(user_id, randint(10000, 99999), 900)
        send_to_email(
            app=current_app,
            subject="Confirmation code",
            recipients=[user.email],
            body=redis_client.get(user_id),
        )

        return (
            BaseResponse(success=True, result="Ok").dict(),
            HTTPStatus.OK,
        )

    @trace("auth_user")
    def auth_user(self, email: str, password: str):
        if not email or not password:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "No email or no password."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        user = self._auth_repository.get_user_by_email(email=email)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist."}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        password = check_password(user.password_hash, password)
        if not password:
            return (
                BaseResponse(
                    success=False, error={"msg": "Invalid password."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )

        if not user.verified_mail:
            return (
                BaseResponse(
                    success=False, error={"msg": "Email is not verified."}
                ).dict(),
                HTTPStatus.CONFLICT,
            )

        user_roles = self.get_user_roles(user.id)

        payload = {
            "user_id": str(user.id),
            "email": email,
            "verified_mail": user.verified_mail,
            "roles": user_roles,
        }
        access_token = create_access_token(identity=payload)
        refresh_token = create_refresh_token(identity=payload)

        response = make_response(
            BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK
        )
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        try:
            user_agent = parse(request.user_agent.string)
        except Exception:
            user_agent = "unknown device"

        self._auth_repository.save_action_to_login_history(
            user_id=str(user.id),
            device_type=check_device_type(user_agent),
            user_agent=str(user_agent),
            action_type=ActionType.LOGIN.value,
        )

        return response

    def logout_user(self, *args):
        access_token = request.cookies.get("access_token_cookie")
        user_id = decode_token(access_token)["sub"]["user_id"]

        jti = get_jwt()["jti"]
        redis_client.set(
            jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
        )

        response = make_response(
            BaseResponse(success=True, result="Ok").dict(),
            HTTPStatus.NO_CONTENT,
        )
        unset_jwt_cookies(response)

        try:
            user_agent = parse(request.user_agent.string)
        except Exception:
            user_agent = "unknown device"

        self._auth_repository.save_action_to_login_history(
            user_id=user_id,
            device_type=check_device_type(user_agent),
            user_agent=str(user_agent),
            action_type=ActionType.LOGOUT.value,
        )

        return response

    def update_access_token(self, identity: dict):
        jti = get_jwt()["jti"]
        redis_client.set(
            jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
        )

        access_token = create_access_token(identity=identity)

        response = make_response(
            BaseResponse(success=True, result="Ok").dict(), HTTPStatus.OK
        )
        set_access_cookies(response, access_token)

        return response
