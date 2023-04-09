from http import HTTPStatus

from flask_restx import Namespace, Resource, fields, reqparse

from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("email", type=str)


checking_mail_model_response = api.model(
    "CheckingMailModelResponse",
    {
        "id": fields.String(required=True),
        "email": fields.String(required=True),
    },
)


@api.route("/checking_mail")
class CheckingMail(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User already exist.",
                checking_mail_model_response,
            ),
            int(HTTPStatus.NOT_FOUND): "User does not exist.",
        }
    )
    @api.param("email", "Почта пользователя")
    def get(self):
        args = parser.parse_args()
        email = args["email"]
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.checking_mail(email)
