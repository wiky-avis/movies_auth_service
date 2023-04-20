from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModelResponse
from src.api.v1.dto.role import (
    InputRoleModel,
    OutputRoleModel,
    OutputUserRoleModel,
    RoleResponse,
    UserRoleResponse,
)
from src.common.decode_auth_token import get_user_roles
from src.common.response import BaseResponse
from src.db import db_models
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService

api = Namespace(name="roles", path="/api/v1/roles")
api.models[InputRoleModel.name] = InputRoleModel
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse
api.models[OutputRoleModel.name] = OutputRoleModel
api.models[RoleResponse.name] = RoleResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


@api.route("", methods=["GET", "POST", "DELETE"])
class Roles(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "List all roles.",
                RoleResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                    "Forbidden.",
                    ErrorModelResponse,
            ),
        },
        description="Получить весь список ролей.",
    )
    @api.header("X-Auth-Token", "JWT токен")
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
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.get_all_roles()

    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Add role.",
                UserRoleResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "Invalid user_id or role_id.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                    "Forbidden.",
                    ErrorModelResponse,
            ),
        },
        description="Назначить пользователю роль.",
    )
    @api.header("X-Auth-Token", "JWT токен")
    @api.expect(InputRoleModel)
    def post(self):
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
        user_id = request.json.get("user_id")
        role_id = request.json.get("role_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.add_role(user_id, role_id)

    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Delete role.",
                UserRoleResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "Invalid user_id or role_id.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                    "Forbidden.",
                    ErrorModelResponse,
            ),
        },
        description="Удалить у пользователя роль.",
    )
    @api.header("X-Auth-Token", "JWT токен")
    @api.expect(InputRoleModel)
    def delete(self):
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
        user_id = request.json.get("user_id")
        role_id = request.json.get("role_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.delete_role(user_id, role_id)
