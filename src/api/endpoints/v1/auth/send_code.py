from http import HTTPStatus

from flask_restx import Namespace, Resource

from src.api.base.dto.base import ErrorModel, ErrorModelResponse
from src.api.base.dto.send_code import SendCodeResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")
api.models[ErrorModel.name] = ErrorModel
api.models[SendCodeResponse.name] = SendCodeResponse


@api.route("/<string:user_id>/send_code", methods=["POST"])
class SendCode(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "The code has been sent.",
                SendCodeResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User not found.",
                ErrorModelResponse,
            ),
        },
        description="Отправка кода подтверждения.",
    )
    def post(self, user_id):
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.send_code(user_id=user_id)
