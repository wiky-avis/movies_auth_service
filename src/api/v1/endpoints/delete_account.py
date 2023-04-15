import logging
from http import HTTPStatus

from flask_restx import Namespace, Resource, fields, reqparse, Model

from src.api.v1.models.dto import base_model_response
from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="v1", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


user_delete_account_model = api.model(
    "DeleteAccountModel",
    {
        "user_id": fields.String(),
        "deleted": fields.Boolean(example=True),
    },
)

api.models[base_model_response.name] = base_model_response

user_delete_account_model_response = api.inherit(
    "DeleteAccountResponse",
    base_model_response,
    {"result": fields.Nested(user_delete_account_model)},
)


@api.route("/delete_account", methods=["DELETE"])
class DeleteAccount(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.NO_CONTENT): (
                "Account is deleted.",
                user_delete_account_model_response,
            ),
            int(HTTPStatus.NOT_FOUND): "User does not exist.",
        },
        description="Удаление аккаунта.",
    )
    def delete(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        auth_user_id = get_user_id(access_token)
        if not auth_user_id:
            logger.warning("Failed to get auth_user_id.")
            return (
                BaseResponse(
                    success=False, error={"msg": "UndefinedUser."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )

        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.delete_account(user_id=auth_user_id)