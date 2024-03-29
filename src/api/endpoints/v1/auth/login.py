from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.api.base.dto.base import (
    BaseModelResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.api.base.dto.user import InputUserAuthModel, UserAuthModelResponse
from src.common.rate_limite import allow_request
from src.common.tracer import trace_request as trace
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
api.models[InputUserAuthModel.name] = InputUserAuthModel
api.models[UserAuthModelResponse.name] = UserAuthModelResponse
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse


@api.route("/login", methods=["POST"])
class Login(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Success.",
                UserAuthModelResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.UNAUTHORIZED): (
                "Invalid password.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.CONFLICT): (
                "Email is not verified.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.TOO_MANY_REQUESTS): (
                "Too Many Requests.",
                ErrorModelResponse,
            ),
        },
        description="Аутентификация пользователя.",
    )
    @api.expect(InputUserAuthModel)
    @allow_request("login")
    @trace("login")
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        localtime = request.json.get("localtime")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.auth_user(
            email=email, password=password, localtime=localtime
        )
