import logging
from http import HTTPStatus

from flask import request
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_restx import Namespace, Resource
from jwt import DecodeError

from src.api.v1.dto.base import ErrorModelResponse
from src.api.v1.dto.role import OutputUserRoleModel, UserRoleResponse
from src.common.collections import get_in
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


logger = logging.getLogger(__name__)

api = Namespace(name="roles", path="/api/v1/roles")
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse


@api.route(
    "/check_permissions",
    methods=[
        "GET",
    ],
)
class CheckPermissions(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "List user role.",
                UserRoleResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.UNAUTHORIZED): (
                "Unauthorized.",
                ErrorModelResponse,
            ),
        },
        description="Список ролей пользователя.",
    )
    def get(self):
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
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.check_permissions(auth_user_id)
