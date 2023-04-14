from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src.api.v1.models.dto import InputUserRegisterModel, UserModelResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="v1", path="/api/v1/users")

input_user_register_model = api.model(
    "InputUserRegister",
    InputUserRegisterModel,
)

user_register_model_response = api.model(
    "UserRegisterResponse",
    UserModelResponse,
)


@api.route("/sign_up", methods=["POST"])
@api.route("/<string:user_id>/sign_up", methods=["PATCH"])
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

    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User approved.",
                user_register_model_response,
            ),
            int(HTTPStatus.BAD_REQUEST): "User does not exist.",
            int(HTTPStatus.BAD_REQUEST): "Password is required.",
            int(HTTPStatus.CONFLICT): "User already verified.",
        },
        description="Полноценная регистрация пользователя.",
    )
    @api.expect(input_user_register_model)
    def patch(self, user_id):
        password = request.json.get("password")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.approve_user(user_id=user_id, password=password)
