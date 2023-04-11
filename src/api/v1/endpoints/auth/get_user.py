from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.models.dto import UserModelResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("email", type=str)


checking_mail_model_response = api.model(
    "CheckingMailResponse",
    UserModelResponse,
)


@api.route("")
class GetUser(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User exist.",
                checking_mail_model_response,
            ),
            int(HTTPStatus.NOT_FOUND): "User does not exist.",
            int(HTTPStatus.BAD_REQUEST): "Email is not valid.",
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
