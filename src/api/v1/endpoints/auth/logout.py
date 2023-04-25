from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from src.api.v1.dto.logout import UserLogoutResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")


@api.route("/logout")
class Logout(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Success.",
                UserLogoutResponse,
            ),
        },
        description="Выход из аккаунта.",
    )
    @jwt_required()
    def get(self):
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.logout_user(self.get)
