from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from gevent import monkey

from src.api.technical.ping import api as ping_api
from src.api.v1.endpoints.auth.checking_mail import api as check_mail
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
    api.add_namespace(check_mail)

    cors.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
