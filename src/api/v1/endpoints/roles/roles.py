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
from src.db import db_models
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
parser.add_argument("user_id", type=str)


@api.route("", methods=["GET", "POST", "DELETE"])
class Roles(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "List all roles.",
                RoleResponse,
            ),
        },
        description="Получить весь список ролей.",
    )
    def get(self):
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
        },
        description="Назначить пользователю роль.",
    )
    @api.expect(InputRoleModel)
    def post(self):
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
        },
        description="Удалить у пользователя роль.",
    )
    @api.expect(InputRoleModel)
    def delete(self):
        user_id = request.json.get("user_id")
        role_id = request.json.get("role_id")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.delete_role(user_id, role_id)
