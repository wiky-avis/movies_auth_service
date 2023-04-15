import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.api.v1.dto.base import ErrorModel, ErrorModelResponse
from src.api.v1.dto.change_data import (
    InputUserChangeData,
    UserChangeDataResponse,
)
from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="v1", path="/api/v1/users")
api.models[InputUserChangeData.name] = InputUserChangeData
api.models[UserChangeDataResponse.name] = UserChangeDataResponse
api.models[ErrorModel.name] = ErrorModel
api.models[ErrorModelResponse.name] = ErrorModelResponse
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


@api.route("/change_data")
class UserChangeData(Resource):
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
    def put(self):
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
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.change_data(
            user_id=auth_user_id,
            new_email=new_email,
        )
