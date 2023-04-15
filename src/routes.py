from flask import Flask
from flask_restx import Api

from src.api.technical.ping import api as ping_api
from src.api.v1.endpoints.change_data import api as change_data
from src.api.v1.endpoints.change_password import api as change_password
from src.api.v1.endpoints.delete_account import api as delete_account
from src.api.v1.endpoints.email_confirmation import api as email_confirmation
from src.api.v1.endpoints.get_list_login_history import (
    api as list_login_history,
)
from src.api.v1.endpoints.get_user import api as get_user
from src.api.v1.endpoints.sign_up import api as sign_up


def attach_routes(app: Flask):
    api = Api(
        app=app,
        title="API Auth",
        description="API для авторизации пользователей",
        doc="/api/swagger/",
        version="1.0.0",
    )
    api.add_namespace(ping_api)
    api.add_namespace(get_user)
    api.add_namespace(sign_up)
    api.add_namespace(list_login_history)
    api.add_namespace(change_data)
    api.add_namespace(change_password)
    api.add_namespace(email_confirmation)
    api.add_namespace(delete_account)
