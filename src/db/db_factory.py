from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData

from src.db import db_models
from src.settings.config import convention


metadata = MetaData(naming_convention=convention)
migrate = Migrate()


def init_db(app: Flask):
    db_models.db.init_app(app)
    migrate.init_app(app, db_models.db)

    return db_models.db
