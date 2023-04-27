import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModelResponse
from src.api.v1.dto.role import OutputUserRoleModel, UserRoleResponse
from src.common.decorators import admin_required
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


logger = logging.getLogger(__name__)

api = Namespace(name="roles", path="/api/v1/roles")
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse
parser = reqparse.RequestParser()
parser.add_argument("user_id", type=str)


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
        description="Список ролей пользователя по user_id.",
    )
    @api.param("user_id", "Id пользователя")
    @admin_required(request)
    def get(self):
        args = parser.parse_args()
        user_id = args.get("user_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.check_permissions(user_id)
