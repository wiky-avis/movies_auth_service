import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModel, ErrorModelResponse
from src.api.v1.dto.login_history import (
    LoginHistoryModel,
    LoginHistoryResponse,
    PaginationModel,
)
from src.common.collections import get_in
from src.common.decode_auth_token import get_decoded_data
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="auth", path="/api/v1/users")
api.models[LoginHistoryModel.name] = LoginHistoryModel
api.models[PaginationModel.name] = PaginationModel
api.models[LoginHistoryResponse.name] = LoginHistoryResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("page", type=int)
parser.add_argument("per_page", type=int)


@api.route("/login_history")
class GetListUserLoginHistory(Resource):
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
        page = args.get("page")
        per_page = args.get("per_page")

        access_token = request.cookies.get("access_token_cookie")
        decoded_token = get_decoded_data(access_token)
        auth_user_id = get_in(decoded_token, "sub", "user_id")
        if not auth_user_id:
            logger.warning("Failed to get auth_user_id.")
            return (
                BaseResponse(
                    success=False, error={"msg": "UndefinedUser."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )

        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.get_list_user_login_history(
            auth_user_id, page, per_page
        )
