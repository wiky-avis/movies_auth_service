from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from gevent import monkey

from src.db.db_factory import init_db
from src.routes import attach_routes


monkey.patch_all(ssl=False)

cors = CORS()

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.Config")
    app.app_context().push()

    jwt.init_app(app)

    init_db(app)
    attach_routes(app)
    cors.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
