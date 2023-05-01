from flask import Flask
from flask_restx import Api

from src.api.endpoints.srv.roles.check_permissions import (
    api as srv_check_permissions,
)
from src.api.endpoints.srv.roles.roles import api as srv_roles
from src.api.endpoints.technical.ping import api as ping_api
from src.api.endpoints.v1.auth.change_password import api as change_password
from src.api.endpoints.v1.auth.email_confirmation import (
    api as email_confirmation,
)
from src.api.endpoints.v1.auth.get_list_login_history import (
    api as list_login_history,
)
from src.api.endpoints.v1.auth.login import api as login
from src.api.endpoints.v1.auth.logout import api as logout
from src.api.endpoints.v1.auth.refresh_token import api as refresh_token
from src.api.endpoints.v1.auth.send_code import api as send_code
from src.api.endpoints.v1.auth.sign_up import api as sign_up
from src.api.endpoints.v1.auth.users import api as users
from src.api.endpoints.v1.oauth.authorize import api as authorize
from src.api.endpoints.v1.oauth.callback import api as callback
from src.api.endpoints.v1.roles.check_permissions import (
    api as check_permissions,
)
from src.api.endpoints.v1.roles.roles import api as roles
from src.api.endpoints.srv.roles.create_new_role import api as srv_create_role
from src.api.endpoints.srv.roles.delete_role import api as srv_delete_role


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
    api.add_namespace(logout)
    api.add_namespace(refresh_token)
    api.add_namespace(login)
    api.add_namespace(sign_up)
    api.add_namespace(list_login_history)
    api.add_namespace(change_password)
    api.add_namespace(email_confirmation)
    api.add_namespace(send_code)
    # role
    api.add_namespace(roles)
    api.add_namespace(check_permissions)
    # oauth
    api.add_namespace(authorize)
    api.add_namespace(callback)
    # srv
    api.add_namespace(srv_roles)
    api.add_namespace(srv_check_permissions)
    api.add_namespace(srv_create_role)
    api.add_namespace(srv_delete_role)
