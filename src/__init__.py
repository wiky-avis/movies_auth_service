from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from flask import Flask

BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATION_DIR = BASE_DIR / "db" / "migrations"

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def init_db(app: Flask):
    """Инициализация базы данных."""
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://app:123qwe@localhost:5432/auth_database'
    db.init_app(app)
    # Migrate(app, db, MIGRATION_DIR, command='db')

    return db
