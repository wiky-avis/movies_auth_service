import logging
from http import HTTPStatus
from uuid import uuid4

from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from gevent import monkey

from src.common.response import BaseResponse
from src.common.tracer import configure_tracer
from src.db.db_factory import init_db
from src.routes import attach_routes
from src.settings.config import DEBUG, ENABLE_TRACING


monkey.patch_all()

cors = CORS()

jwt = JWTManager()


def init_tracer(app: Flask):
    if ENABLE_TRACING:
        configure_tracer(app)
        logging.info("Tracing is enabled")
    else:
        logging.info("Tracing is disabled")


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.Config")
    app.app_context().push()

    jwt.init_app(app)

    init_db(app)
    attach_routes(app)
    cors.init_app(app)

    init_tracer(app)

    return app


app = create_app()


@app.before_request
def before_request():
    if DEBUG:
        request.environ["HTTP_X_REQUEST_ID"] = str(uuid4())

    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return (
            BaseResponse(
                success=False, error={"msg": "Request id is required."}
            ).dict(),
            HTTPStatus.BAD_REQUEST,
        )


if __name__ == "__main__":
    app.run()
