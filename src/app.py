from flask import Flask
from flask_cors import CORS
from gevent import monkey

from src.db.db_factory import init_db
from src.routes import attach_routes


monkey.patch_all()

cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.app_context().push()

    init_db(app)
    attach_routes(app)
    cors.init_app(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
