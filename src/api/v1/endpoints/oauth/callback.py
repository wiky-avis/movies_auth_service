from flask import request
from flask_restx import Namespace, Resource

from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.oauth_service import OAuthService
from src.settings import get_service_config


api = Namespace(name="roles", path="/api/v1/users")


@api.route(
    "/callback/<string:provider_name>",
    methods=[
        "GET",
    ],
)
class OAuthCallback(Resource):
    def get(self, provider_name):
        auth_code = request.args.get("code")
        config = get_service_config(provider_name)
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        oauth_service = OAuthService(
            config=config,
            auth_repository=auth_repository,
            roles_repository=roles_repository,
            provider_name=provider_name,
        )
        return oauth_service.callback(
            auth_code,
            state=request.args.get("state"),
        )
