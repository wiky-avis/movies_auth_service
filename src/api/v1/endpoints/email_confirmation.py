from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.models.dto import (
    EmailConfirmationResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.common.response import BaseResponse
from src.db.redis import redis_client


api = Namespace(name="v1", path="/api/v1/users")
api.models[EmailConfirmationResponse.name] = EmailConfirmationResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("code", type=str)


@api.route("/<string:user_id>/mail")
class EmailConfirmation(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Email confirmed.",
                EmailConfirmationResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "Email not found.",
                ErrorModelResponse,
            ),
        },
        description="Подтверждение почты.",
    )
    @api.param("code", "Код подтверждения почты")
    def put(self, user_id):
        args = parser.parse_args()
        secret_code = args.get("code")

        code_in_redis = redis_client.get(user_id)
        if code_in_redis and secret_code == code_in_redis:
            return (
                BaseResponse(success=True, result="Ok").dict(),
                HTTPStatus.OK,
            )
        return BaseResponse(success=False).dict(), HTTPStatus.NOT_FOUND
