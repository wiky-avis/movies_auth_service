from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from src import settings
from src.api.base.dto.base import ErrorModelResponse
from src.api.base.dto.role import (
    InputCreateRoleModel,
    OutputRoleModel,
    OutputUserRoleModel,
)
from src.common.decorators import token_required
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.role_service import RolesService


api = Namespace(name="roles", path="/api/srv/roles")
api.models[InputCreateRoleModel.name] = InputCreateRoleModel
api.models[OutputUserRoleModel.name] = OutputUserRoleModel


@api.route(
    "/create_role",
    methods=[
        "POST",
    ],
)
class CreateRole(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.CREATED): (
                "Create role.",
                OutputRoleModel,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "Did not pass role_name.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.FORBIDDEN): (
                "Forbidden.",
                ErrorModelResponse,
            ),
        },
        description="Создать роль в бд.",
    )
    @api.expect(InputCreateRoleModel)
    @token_required(request, settings.AUTH_SRV_TOKENS)
    def post(self):
        role_name = request.json.get("role_name")
        description = request.json.get("description")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        role_service = RolesService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return role_service.create_role(
            role_name=role_name, description=description
        )
