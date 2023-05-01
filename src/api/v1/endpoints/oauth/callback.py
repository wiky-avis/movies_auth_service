from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.api.v1.dto.base import (
    BaseModelResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.api.v1.dto.user import (
    BaseUserModel,
    TemporaryUserModel,
    TemporaryUserModelResponse,
)
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.oauth_service import OAuthService
from src.settings import get_service_config


api = Namespace(name="oauth", path="/api/v1/users")
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[TemporaryUserModel.name] = TemporaryUserModel
api.models[TemporaryUserModelResponse.name] = TemporaryUserModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse


@api.route(
    "/callback/<string:provider_name>",
    methods=[
        "GET",
    ],
)
class OAuthCallback(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User created or exists.",
                TemporaryUserModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "Unidentified provider. | Error getting code.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "Error getting user data. Invalid auth_code or external service error.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.UNAUTHORIZED): (
                "Error getting user info. Invalid token or external service error.",
                ErrorModelResponse,
            ),
        },
        description="Авторизация OAuth2. Получает данные о пользователе из соц сетей и создает нового пользователя.",
    )
    def get(self, provider_name):
        auth_code = request.args.get("code")
        config = get_service_config(provider_name)
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        oauth_service = OAuthService(
            config=config,
            auth_repository=auth_repository,
            roles_repository=roles_repository,
            provider_name=provider_name,
        )
        return oauth_service.callback(
            auth_code,
            state=request.args.get("state"),
        )
