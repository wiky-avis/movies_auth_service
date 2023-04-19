from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModel, ErrorModelResponse
from src.api.v1.dto.email_confirmation import EmailConfirmationResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="v1", path="/api/v1/users")
api.models[EmailConfirmationResponse.name] = EmailConfirmationResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("code", type=str)


@api.route("/<string:user_id>/mail")
class EmailConfirmation(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Email confirmed.",
                EmailConfirmationResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "Email not found.",
                ErrorModelResponse,
            ),
        },
        description="Подтверждение почты.",
    )
    @api.param("code", "Код подтверждения почты")
    def post(self, user_id):
        args = parser.parse_args()
        secret_code = args.get("code")

        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.email_confirmation(
            secret_code=secret_code, user_id=user_id
        )
