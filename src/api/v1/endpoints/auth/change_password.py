import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModel, ErrorModelResponse
from src.api.v1.dto.change_data import (
    InputUserChangePassword,
    UserChangePasswordResponse,
)
from src.common.collections import get_in
from src.common.decode_auth_token import get_decoded_data
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="auth", path="/api/v1/users")
api.models[InputUserChangePassword.name] = InputUserChangePassword
api.models[UserChangePasswordResponse.name] = UserChangePasswordResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


@api.route("/change_password")
class UserChangeData(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Password is changed.",
                UserChangePasswordResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "No new password or no old password.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.UNAUTHORIZED): (
                "Invalid password.",
                ErrorModelResponse,
            ),
        },
        description="Изменение пароля.",
    )
    @api.header("X-Auth-Token", "JWT токен")
    @api.expect(InputUserChangePassword)
    def patch(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        decoded_data = get_decoded_data(access_token)
        auth_user_id = get_in(decoded_data, "UserId")
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
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.change_password(
            user_id=auth_user_id,
            old_password=old_password,
            new_password=new_password,
        )
