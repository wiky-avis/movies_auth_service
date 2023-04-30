from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.common.response import BaseResponse
from src.common.services.oauth_service import OAuthService
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.settings import get_service_config


api = Namespace(name="roles", path="/api/v1/users")


@api.route(
    "/callback/<string:provider_name>",
    methods=[
        "GET",
    ],
)
class OAuthCallback(Resource):
    def get(self, provider_name):
        yandex_code = request.args.get("code")
        config = get_service_config(provider_name)
        auth_repository = AuthRepository(db_models.db)
        result = OAuthService(
            config=config,
            auth_repository=auth_repository,
            provider_name=provider_name,
        )
        # yandex,  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.0.2318 Yowser/2.5 Safari/537.36
        print(request.args.get("state"), request.headers.get("User-Agent"))
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
