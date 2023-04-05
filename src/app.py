from flask import Flask
from flask_restx import Api
from gevent import monkey

from src.api.v1.ping import api as ping_api

monkey.patch_all()

app = Flask(__name__)

api = Api(
    app=app,
    title="API Auth",
    description="API для авторизации пользователей",
    doc="/api/swagger/",
    version="1.0.0",
)
api.add_namespace(ping_api)


if __name__ == "__main__":
    app.run()
