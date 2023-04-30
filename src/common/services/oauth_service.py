import logging
from http import HTTPStatus
from urllib.parse import urlencode, urljoin

import requests
from flask import redirect

from src import settings
from src.api.v1.models.user import UserResponse
from src.common.collections import get_in
from src.common.gen_password import generate_random_string
from src.common.response import BaseResponse
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.models import PoviderName


logger = logging.getLogger(__name__)


class OAuthService:
    def __init__(
        self,
        config: settings.BaseOAuthConfig,
        auth_repository: AuthRepository,
        roles_repository: RolesRepository,
        provider_name: str,
    ):
        self._config = config
        self._auth_repository = auth_repository
        self._roles_repository = roles_repository
        self._provider_name = provider_name

    @staticmethod
    def build_url(base_url: str = None, **kwargs):
        params = urlencode(kwargs)
        return urljoin(base_url, f"?{params}")

    def get_params(self):
        params = dict()
        if self._provider_name == PoviderName.YANDEX:
            params = dict(
                client_id=self._config.client_id,
                display="popup",
                response_type="code",
                state="yandex",
            )
        elif self._provider_name == PoviderName.GOOGLE:
            params = dict(
                client_id=self._config.client_id,
                access_type="offline",
                response_type="code",
                redirect_uri=self._config.redirect_uri,
                scope=self._config.scope,
                state="google",
            )
        return params

    def get_token(self, auth_code):
        data = urlencode(
            dict(
                grant_type=self._config.grant_type or "",
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                code=auth_code,
            )
        )
        token = requests.post(
            url=self._config.url_token,
            data=data,
        ).json()
        return token

    def get_user_info(self, data):
        user_info = dict()
        access_token = get_in(data, "access_token")
        if self._provider_name == PoviderName.YANDEX:
            user_info = requests.get(
                url=self._config.url_user_info,
                params=urlencode(
                    dict(Authorization="OAuth", oauth_token=access_token)
                ),
            )
        elif self._provider_name == PoviderName.GOOGLE:
            token_type = get_in(data, "token_type")
            user_info = requests.get(
                url=self._config.url_user_info,
                headers=dict(Authorization=f"{token_type} {access_token}"),
            ).json()
        return user_info.json()

    def authorize(self):
        params = self.get_params()
        url = self.build_url(base_url=self._config.redirect_auth_uri, **params)
        return redirect(url, code=302)

    def callback(self, auth_code: str, state: str):
        if not auth_code:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "Error getting code."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        data = self.get_token(auth_code)
        if not data:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "Error getting data."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user_data = self.get_user_info(data)
        if not user_data:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "Error getting code."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        email = (
            get_in(user_data, "email")
            or get_in(user_data, "default_email")
            or get_in(user_data, "emails", 0)
        )

        return self.oauth_authorize(
            email=email,
            login=get_in(user_data, "login"),
            social_id=str(get_in(user_data, "id")),
            social_name=state.upper(),
        )

    def oauth_authorize(self, email, login, social_id, social_name):
        old_user = self._auth_repository.get_user_by_universal_login(
            username=login, email=email
        )
        if old_user:
            social_account = (
                self._auth_repository.get_social_account_by_user_id(
                    old_user.id
                )
            )
            if not social_account:
                self._auth_repository.create_social_account(
                    social_id, social_name, old_user.id
                )

            roles_ids = self._roles_repository.get_ids_roles_by_user_id(
                old_user.id
            )
            user_roles = self._roles_repository.get_role_names_by_ids(
                roles_ids
            )
            user = UserResponse(
                id=str(old_user.id),
                email=old_user.email,
                roles=user_roles,
                verified_mail=old_user.verified_mail,
                registered_on=str(old_user.registered_on),
            )
        else:
            generated_password = generate_random_string()
            role = RoleType.ROLE_PORTAL_USER.value
            self._auth_repository.create_user(email=email)
            new_user = self._auth_repository.get_user_by_email(email=email)
            if not new_user:
                return (
                    BaseResponse(
                        success=False, error={"msg": "New user does not exist"}
                    ).dict(),
                    HTTPStatus.NOT_FOUND,
                )
            self._auth_repository.create_social_account(
                social_id, social_name, new_user.id
            )
            self._auth_repository.set_password(
                user=new_user, password=generated_password
            )
            self._roles_repository.set_role_by_role_name(new_user, role)
            roles_ids = self._roles_repository.get_ids_roles_by_user_id(
                new_user.id
            )
            user_roles = self._roles_repository.get_role_names_by_ids(
                roles_ids
            )
            user = UserResponse(
                id=str(new_user.id),
                email=new_user.email,
                roles=user_roles,
                verified_mail=new_user.verified_mail,
                registered_on=str(new_user.registered_on),
            )
        return (
            BaseResponse(success=True, result=user).dict(),
            HTTPStatus.CREATED,
        )
