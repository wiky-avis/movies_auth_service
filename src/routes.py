from flask import Flask
from flask_restx import Api

from src.api.technical.ping import api as ping_api
from src.api.v1.endpoints.auth.change_password import api as change_password
from src.api.v1.endpoints.auth.email_confirmation import (
    api as email_confirmation,
)
from src.api.v1.endpoints.auth.get_list_login_history import (
    api as list_login_history,
)
from src.api.v1.endpoints.auth.sign_up import api as sign_up
from src.api.v1.endpoints.auth.users import api as users
from src.api.v1.endpoints.role.add_role import api as add_role
from src.api.v1.endpoints.role.check_permissions import (
    api as check_permissions,
)
from src.api.v1.endpoints.role.delete_role import api as delete_role


def attach_routes(app: Flask):
    api = Api(
        app=app,
        title="API Auth",
        description="API для авторизации пользователей",
        doc="/api/swagger/",
        version="1.0.0",
    )
    # auth
    api.add_namespace(ping_api)
    api.add_namespace(users)
    api.add_namespace(sign_up)
    api.add_namespace(list_login_history)
    api.add_namespace(change_password)
    api.add_namespace(email_confirmation)
    # role
    api.add_namespace(add_role)
    api.add_namespace(check_permissions)
    api.add_namespace(delete_role)
