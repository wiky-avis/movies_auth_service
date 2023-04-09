from flask import request
from flask_restx import Namespace, Resource, fields

from src.db.db_factory import db
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="registration", path="/api/v1/users")

input_user_register_model = api.model(
    "InputUserRegisterModel",
    {
        "email": fields.String(required=True, description="Почта"),
        "password": fields.String(required=False, description="Пароль"),
        "role": fields.String(required=False, description="Роль пользователя"),
    },
)


@api.route("/sign_up")
class SignUp(Resource):
    @api.expect(input_user_register_model)
    def post(self):
        email = request.json.get("email")
        role = RoleType.ROLE_TEMPORARY_USER.value
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        user = auth_service.get_register_user_or_temporary_user(
            email=email, role_name=role
        )

        return {
            "success": True,
            "result": user,
        }
