from http import HTTPStatus

from flask_restx import Namespace, Resource, fields, reqparse

from src.common.response import BaseResponse
from src.db.redis import redis_client


api = Namespace(name="v1", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("code", type=str)


email_confirmation_model_response = api.model(
    "EmailConfirmationResponse",
    {
        "result": fields.String(example="Ok"),
    },
)


@api.route("/<string:user_id>/mail")
class EmailConfirmation(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Email confirmed.",
                email_confirmation_model_response,
            ),
            int(HTTPStatus.NOT_FOUND): ("Email not found.",),
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
