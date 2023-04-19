from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData

from src.config import convention
from src.db import db_models


metadata = MetaData(naming_convention=convention)
migrate = Migrate()


def init_db(app: Flask):
    db_models.db.init_app(app)
    migrate.init_app(app, db_models.db)

    return db_models.db
