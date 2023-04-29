from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src import settings
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.services.yandex_oauth_service import YandexOAuthService


api = Namespace(name="roles", path="/api/v1/users")


@api.route(
    "/oauth/yandex",
    methods=[
        "GET",
    ],
)
class OAuthYandex(Resource):
    def get(self):
        auth_repository = AuthRepository(db_models.db)
        result = YandexOAuthService(
            config=settings.YandexOAuthConfig(),
            auth_repository=auth_repository,
        )
        return result.authorize()


@api.route(
    "/callback/yandex",
    methods=[
        "GET",
    ],
)
class CallbackYandex(Resource):
    def get(self):
        yandex_code = request.args.get("code")
        auth_repository = AuthRepository(db_models.db)
        result = YandexOAuthService(
            config=settings.YandexOAuthConfig(),
            auth_repository=auth_repository,
        )
        if yandex_code:
            print(yandex_code)
            res = result.callback(
                yandex_code,
                user_agent=request.headers.get("User-Agent"),
                state=request.args.get("state"),
            )
            return (
                BaseResponse(
                    success=True,
                    result=res,
                ).dict(),
                HTTPStatus.OK,
            )
        else:
            return (
                BaseResponse(
                    success=False,
                    error={"msg": "Error getting code."},
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
