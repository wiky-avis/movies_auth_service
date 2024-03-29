from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.api.base.dto.base import (
    BaseModelResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.api.base.dto.user import (
    BaseUserModel,
    InputUserRegisterModel,
    TemporaryUserModel,
    TemporaryUserModelResponse,
)
from src.common.rate_limite import allow_request
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
api.models[InputUserRegisterModel.name] = InputUserRegisterModel
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[TemporaryUserModel.name] = TemporaryUserModel
api.models[TemporaryUserModelResponse.name] = TemporaryUserModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse


@api.route("/sign_up", methods=["POST"])
class SignUp(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.CREATED): (
                "User created.",
                TemporaryUserModelResponse,
            ),
            int(HTTPStatus.CONFLICT): (
                "User already exists.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.TOO_MANY_REQUESTS): (
                "Too Many Requests.",
                ErrorModelResponse,
            ),
        },
        description="Создание временного пользователя.",
    )
    @api.expect(InputUserRegisterModel)
    @allow_request("sign_up")
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        localtime = request.json.get("localtime")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.register_temporary_user(
            email=email, password=password, localtime=localtime
        )
