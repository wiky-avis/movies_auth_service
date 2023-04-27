from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from src.api.v1.dto.refresh import UpdateAccessTokenResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
api.models[UpdateAccessTokenResponse.name] = UpdateAccessTokenResponse


@api.route("/refresh", methods=["POST"])
class Refresh(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Success.",
                UpdateAccessTokenResponse,
            ),
        },
        description="Обновление access-токена.",
    )
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.update_access_token(identity=identity)
