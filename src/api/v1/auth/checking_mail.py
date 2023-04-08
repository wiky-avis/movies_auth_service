from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.common.response import BaseResponse
from src.db.db_factory import db
from src.models.db_models import User


api = Namespace(name="auth", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("email", type=str)


@api.route("/checking_mail")
@api.param("email", "Почта пользователя")
class CheckingMail(Resource):
    def get(self):
        args = parser.parse_args()
        email = args["email"]
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict()
            ), HTTPStatus.NOT_FOUND
        return BaseResponse(success=True, data=user).dict(), HTTPStatus.OK
