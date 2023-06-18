from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src import settings
from src.api.base.dto.base import (
    BaseModelResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.api.base.dto.user import (
    BaseUserModel,
    RegisteredUserModel,
    RegisteredUserModelResponse,
)
from src.common.decorators import token_required
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="users", path="/api/srv/users")
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[RegisteredUserModel.name] = RegisteredUserModel
api.models[RegisteredUserModelResponse.name] = RegisteredUserModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("user_id", type=str)


@api.route("", methods=["GET"])
class Users(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User exist.",
                RegisteredUserModelResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "User id is not valid.",
                ErrorModelResponse,
            ),
        },
        description="Получение информации о пользователе по его id.",
    )
    @api.param("user_id", "Id пользователя")
    @token_required(request, settings.AUTH_SRV_TOKENS)
    def get(self):
        args = parser.parse_args()
        user_id = args.get("user_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.get_user_by_id(user_id)
