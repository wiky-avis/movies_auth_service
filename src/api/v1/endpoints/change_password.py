import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="v1", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


input_user_chancge_password_model = api.model(
    "InputUserChangePassword",
    {
        "old_password": fields.String(description="Пароль"),
        "new_password": fields.String(description="Пароль"),
    },
)


@api.route("/change_password")
class UserChangeData(Resource):
    @api.expect(input_user_chancge_password_model)
    def put(self):
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
        old_password = request.json.get("old_password")
        new_password = request.json.get("new_password")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.change_password(
            user_id=auth_user_id,
            old_password=old_password,
            new_password=new_password,
        )
