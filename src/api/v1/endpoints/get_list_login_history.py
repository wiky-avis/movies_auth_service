import logging
from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.api.v1.models.dto import (
    ErrorModel,
    ErrorModelResponse,
    LoginHistoryModel,
    LoginHistoryResponse,
    PaginationModel,
)
from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="v1", path="/api/v1/users")
api.models[LoginHistoryModel.name] = LoginHistoryModel
api.models[PaginationModel.name] = PaginationModel
api.models[LoginHistoryResponse.name] = LoginHistoryResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")
parser.add_argument("page", type=int)
parser.add_argument("per_page", type=int)


@api.route("/login_history")
class GetListUserLoginHistory(Resource):
    @api.param("X-Auth-Token", "JWT токен")
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "List user login history.",
                LoginHistoryResponse,
            ),
            int(HTTPStatus.UNAUTHORIZED): (
                "UndefinedUser.",
                ErrorModelResponse,
            ),
        },
        description="История входов пользователя в систему.",
    )
    @api.param("page", "Номер страницы")
    @api.param("per_page", "Количество записей на странице")
    def get(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        page = args.get("page")
        per_page = args.get("per_page")

        auth_user_id = get_user_id(access_token)
        if not auth_user_id:
            logger.warning("Failed to get auth_user_id.")
            return (
                BaseResponse(
                    success=False, error={"msg": "UndefinedUser."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )

        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.get_list_user_login_history(
            auth_user_id, page, per_page
        )
