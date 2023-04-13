from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from gevent import monkey

from src.api.technical.ping import api as ping_api
from src.api.v1.endpoints.auth.get_list_login_history import (
    api as list_login_history,
)
from src.api.v1.endpoints.auth.get_user import api as get_user
from src.api.v1.endpoints.change_data import api as change_data
from src.api.v1.endpoints.change_password import api as change_password
from src.api.v1.endpoints.registration.sign_up import api as sign_up
from src.db.db_factory import init_db


monkey.patch_all()

cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.app_context().push()

    init_db(app)

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

    cors.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
