from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from pydantic import BaseModel

from src.db.db_factory import db
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService


api = Namespace(name="change_data", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("X-Auth-Token", location="headers")


input_user_register_model = api.model(
    "InputUserRegister",
    {
        "email": fields.String(description="Почта"),
        "old_password": fields.String(description="Пароль"),
        "new_password": fields.String(description="Пароль"),
    },
)


class ChangeData(BaseModel):
    email: str
    old_password: str
    new_password: str


@api.route("/<string:user_id>/change_data")
class UserChangeData(Resource):
    def put(self, user_id):
        email = request.json.get("email")
        old_password = request.json.get("old_password")
        new_password = request.json.get("new_password")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)
        return auth_service.change_data_user(
            user_id=user_id,
            email=email,
            old_password=old_password,
            new_password=new_password,
        )
