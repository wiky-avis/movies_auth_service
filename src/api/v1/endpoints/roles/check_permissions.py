from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModelResponse
from src.api.v1.dto.role import OutputUserRoleModel, UserRoleResponse
from src.common.decode_auth_token import get_user_roles
from src.common.response import BaseResponse
from src.db import db_models
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


api = Namespace(name="roles", path="/api/v1/roles")
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse
parser = reqparse.RequestParser()
parser.add_argument("user_id", type=str)
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
            int(HTTPStatus.BAD_REQUEST): (
                "user_id is not valid.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                "Forbidden.",
                ErrorModelResponse,
            ),
        },
        description="Список ролей пользователя.",
    )
    @api.header("X-Auth-Token", "JWT токен")
    @api.param("user_id", "Id пользователя")
    def get(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        roles = get_user_roles(access_token)
        if RoleType.ROLE_PORTAL_ADMIN not in roles:
            return (
                BaseResponse(
                    success=False, error={"msg": "Forbidden."}
                ).dict(),
                HTTPStatus.FORBIDDEN,
            )
        user_id = args.get("user_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.check_permissions(user_id)
