from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.api.base.dto.base import ErrorModel, ErrorModelResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.oauth_service import OAuthService
from src.settings import get_service_config


api = Namespace(name="oauth", path="/api/v1/users")
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse


@api.route(
    "/authorize/<string:provider_name>",
    methods=[
        "GET",
    ],
)
class OAuthAuthorize(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.FOUND): "Success redirect.",
            int(HTTPStatus.BAD_REQUEST): (
                "Unidentified provider.",
                ErrorModelResponse,
            ),
        },
        description="Авторизация OAuth2. Редиректит на страницу провайдера.",
    )
    def get(self, provider_name):
        config = get_service_config(provider_name)
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        oauth_service = OAuthService(
            config=config,
            auth_repository=auth_repository,
            roles_repository=roles_repository,
            provider_name=provider_name,
        )
        return oauth_service.authorize()
