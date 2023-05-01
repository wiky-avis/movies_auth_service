from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src import settings
from src.api.base.dto.base import ErrorModelResponse
from src.api.base.dto.role import (
    InputRoleModel,
    OutputRoleModel,
    OutputUserRoleModel,
    RoleResponse,
    UserRoleResponse,
)
from src.common.decorators import token_required
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


api = Namespace(name="roles", path="/api/srv/roles")
api.models[InputRoleModel.name] = InputRoleModel
api.models[OutputUserRoleModel.name] = OutputUserRoleModel
api.models[UserRoleResponse.name] = UserRoleResponse
api.models[OutputRoleModel.name] = OutputRoleModel
api.models[RoleResponse.name] = RoleResponse


@api.route(
    "/delete_role/<string:role_id>",
    methods=[
        "DELETE",
    ],
)
class RemoveRole(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.NO_CONTENT): "Role removed.",
            int(HTTPStatus.BAD_REQUEST): (
                "Did not pass role_id.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                "Forbidden.",
                ErrorModelResponse,
            ),
        },
        description="Удалить роль из бд.",
    )
    @token_required(request, settings.AUTH_SRV_TOKENS)
    def delete(self, role_id):
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.remove_role(role_id)
