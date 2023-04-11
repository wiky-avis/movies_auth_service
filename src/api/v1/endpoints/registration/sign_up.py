from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.api.v1.models.dto import InputUserRegisterModel, UserModelResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="registration", path="/api/v1/users")

input_user_register_model = api.model(
    "InputUserRegister",
    InputUserRegisterModel,
)

user_register_model_response = api.model(
    "UserRegisterResponse",
    UserModelResponse,
)


@api.route("/sign_up")
class SignUp(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.CREATED): (
                "User created.",
                user_register_model_response,
            ),
            int(HTTPStatus.CONFLICT): "User already exists.",
        },
        description="Создание временного пользователя.",
    )
    @api.expect(input_user_register_model)
    def post(self):
        email = request.json.get("email")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.register_temporary_user(email=email)
