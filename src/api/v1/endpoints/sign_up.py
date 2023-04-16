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
    InputUserRegisterModel,
    RegisteredUserModel,
    RegisteredUserModelResponse,
    TemporaryUserModel,
    TemporaryUserModelResponse,
)
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="v1", path="/api/v1/users")
api.models[InputUserRegisterModel.name] = InputUserRegisterModel
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[RegisteredUserModel.name] = RegisteredUserModel
api.models[TemporaryUserModel.name] = TemporaryUserModel
api.models[RegisteredUserModelResponse.name] = RegisteredUserModelResponse
api.models[TemporaryUserModelResponse.name] = TemporaryUserModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse


@api.route("/sign_up", methods=["POST"])
@api.route("/<string:user_id>/sign_up", methods=["PATCH"])
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
        },
        description="Создание временного пользователя.",
    )
    @api.expect(InputUserRegisterModel)
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.register_temporary_user(
            email=email, password=password
        )
