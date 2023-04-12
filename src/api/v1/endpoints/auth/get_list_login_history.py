import logging
from http import HTTPStatus

from flask_restx import Namespace, Resource, reqparse

from src.common.decode_auth_token import get_user_id
from src.common.generate_auth_token import generate_auth_token
from src.common.response import BaseResponse
from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


logger = logging.getLogger(__name__)


api = Namespace(name="auth", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")
parser.add_argument("page", type=int)
parser.add_argument("per_page", type=int)


@api.route("/<string:user_id>/login_history")
class GetListUserLoginHistory(Resource):
    def get(self, user_id):
        args = parser.parse_args()
        print(generate_auth_token(id=user_id))
        access_token = args.get("X-Auth-Token")
        page = args.get("page")
        per_page = args.get("per_page")

        auth_user_id = get_user_id(access_token)
        print(auth_user_id)
        if not auth_user_id:
            logger.warning("Failed to get auth_user_id: user_id %s.", user_id)
            return (
                BaseResponse(
                    success=False, error={"msg": "UndefinedUser."}
                ).dict(),
                HTTPStatus.UNAUTHORIZED,
            )
        if auth_user_id != user_id:
            logger.warning(
                "auth_user_id is not equal to user_id: user_id %s.", user_id
            )
            return (
                BaseResponse(
                    success=False, error={"msg": "Forbidden."}
                ).dict(),
                HTTPStatus.FORBIDDEN,
            )

        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.get_list_user_login_history(user_id, page, per_page)
