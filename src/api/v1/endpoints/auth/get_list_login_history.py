from flask_restx import Namespace, Resource

from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="auth", path="/api/v1/users")


@api.route("/<int:user_id>/login_history")
class GetListUserLoginHistory(Resource):
    def get(self, user_id):
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return {}
