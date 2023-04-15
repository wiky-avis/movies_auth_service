from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.models.dto import (
    BaseModelResponse,
    BaseUserModel,
    ErrorModel,
    ErrorModelResponse,
    RegisteredUserModel,
    RegisteredUserModelResponse,
)
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="v1", path="/api/v1/users")
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[RegisteredUserModel.name] = RegisteredUserModel
api.models[RegisteredUserModelResponse.name] = RegisteredUserModelResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("email", type=str)


@api.route("")
class GetUser(Resource):
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
                "Email is not valid.",
                ErrorModelResponse,
            ),
        },
        description="Получение информации о пользователе по email адресу.",
    )
    @api.param("email", "Email адрес")
    def get(self):
        args = parser.parse_args()
        email = args.get("email")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.get_user_by_email(email)
