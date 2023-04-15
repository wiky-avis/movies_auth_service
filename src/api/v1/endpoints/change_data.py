import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from src.api.v1.models.dto import base_model_response
from src.common.decode_auth_token import get_user_id
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="v1", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")

api.models[base_model_response.name] = base_model_response


input_user_change_data_model = api.model(
    "InputUserChangeData",
    {
        "email": fields.String(description="Почта"),
    },
)

user_change_data_model_response = api.inherit(
    "UserChangeDataResponse",
    base_model_response,
    {
        "result": fields.String(example="Ok"),
    },
)


@api.route("/change_data")
class UserChangeData(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Data is changed.",
                user_change_data_model_response,
            ),
            int(HTTPStatus.NOT_FOUND): "User does not exist.",
            int(HTTPStatus.BAD_REQUEST): "No new email.",
            int(HTTPStatus.CONFLICT): "User with this email already exists.",
        },
        description="Изменение данных.",
    )
    @api.expect(input_user_change_data_model)
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
