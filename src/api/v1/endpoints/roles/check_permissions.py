import logging
from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModelResponse
from src.api.v1.dto.role import OutputUserRoleModel, UserRoleResponse
from src.common.collections import get_in
from src.common.decode_auth_token import get_decoded_data
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


logger = logging.getLogger(__name__)

api = Namespace(name="roles", path="/api/v1/roles")
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


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
    @api.header("X-Auth-Token", "JWT токен")
    def get(self):
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
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.check_permissions(auth_user_id)
