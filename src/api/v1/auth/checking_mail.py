from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.auth.dto import checking_mail_model
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("email", type=str)


@api.route("/checking_mail")
@api.param("email", "Почта пользователя")
class CheckingMail(Resource):
    @api.response(
        int(HTTPStatus.OK), "User already exist.", checking_mail_model
    )
    @api.response(int(HTTPStatus.NOT_FOUND), "User does not exist.")
    def get(self):
        args = parser.parse_args()
        email = args["email"]
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.checking_mail(email)
