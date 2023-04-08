from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.common.response import BaseResponse
from src.models.user import User

api = Namespace(name="v1", path="/api/users/v1")


@api.route(
    "/checking_mail", description="Проверяет, существует ли такой пользователь"
)
@api.param("email", description="Почта пользователя")
class CheckingMail(Resource):
    def get(self, email):
        user = User.find_by_email(email)
        if not user:
            return (
                BaseResponse(success=False, error=user.error_message).dict()
            ), HTTPStatus.NOT_FOUND
        return BaseResponse(success=True, data=user).dict(), HTTPStatus.OK
