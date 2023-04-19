import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import (
    BaseModelResponse,
    ErrorModel,
    ErrorModelResponse,
)
from src.api.v1.dto.change_data import (
    InputUserChangeData,
    UserChangeDataResponse,
)
from src.api.v1.dto.user import (
    BaseUserModel,
    RegisteredUserModel,
    RegisteredUserModelResponse,
)
from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db import db_models
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)

api = Namespace(name="v1", path="/api/v1/users")
api.models[BaseModelResponse.name] = BaseModelResponse
api.models[BaseUserModel.name] = BaseUserModel
api.models[RegisteredUserModel.name] = RegisteredUserModel
api.models[RegisteredUserModelResponse.name] = RegisteredUserModelResponse
api.models[InputUserChangeData.name] = InputUserChangeData
api.models[UserChangeDataResponse.name] = UserChangeDataResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")
parser.add_argument("email", type=str)


@api.route("", methods=["GET", "DELETE", "PATCH"])
class Users(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "User exist.",
                RegisteredUserModelResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): (
                "Email is not valid.",
                ErrorModelResponse,
            ),
        },
        description="Получение информации о пользователе по email адресу.",
    )
    @api.param("email", "Email адрес")
    def get(self):
        args = parser.parse_args()
        email = args.get("email")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.get_user_by_email(email)

    @api.doc(
        responses={
            int(HTTPStatus.NO_CONTENT): "Account is deleted.",
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
        },
        description="Удаление аккаунта.",
    )
    @api.param("X-Auth-Token", "JWT токен")
    def delete(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        auth_user_id = get_user_id(access_token)
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
        return auth_service.delete_account(user_id=auth_user_id)

    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Data is changed.",
                UserChangeDataResponse,
            ),
            int(HTTPStatus.NOT_FOUND): (
                "User does not exist.",
                ErrorModelResponse,
            ),
            int(HTTPStatus.BAD_REQUEST): ("No new email.", ErrorModelResponse),
            int(HTTPStatus.CONFLICT): (
                "User with this email already exists.",
                ErrorModelResponse,
            ),
        },
        description="Изменение данных.",
    )
    @api.param("X-Auth-Token", "JWT токен")
    @api.expect(InputUserChangeData)
    def patch(self):
        args = parser.parse_args()
        access_token = args.get("X-Auth-Token")
        auth_user_id = get_user_id(access_token)
        if not auth_user_id:
            logger.warning("Failed to get auth_user_id.")
            return (
                BaseResponse(
                    success=False, error={"msg": "UndefinedUser."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )

        new_email = request.json.get("email")
        auth_repository = AuthRepository(db_models.db)
        roles_repository = RolesRepository(db_models.db)
        auth_service = AuthService(
            auth_repository=auth_repository, roles_repository=roles_repository
        )
        return auth_service.change_data(
            user_id=auth_user_id,
            new_email=new_email,
        )
