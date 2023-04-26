import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_restx import Namespace, Resource
from jwt import DecodeError

from src.api.v1.dto.base import ErrorModel, ErrorModelResponse
from src.api.v1.dto.change_data import (
    InputUserChangePassword,
    UserChangePasswordResponse,
)
from src.common.collections import get_in
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
    @api.expect(InputUserChangePassword)
    def patch(self):
        access_token = request.cookies.get("access_token_cookie")
        try:
            decoded_token = decode_token(access_token)
        except (DecodeError, JWTDecodeError):
            decoded_token = None
        auth_user_id = get_in(decoded_token, "sub", "user_id")
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
