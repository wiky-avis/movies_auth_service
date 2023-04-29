from datetime import datetime

import psycopg2
import pytest
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from psycopg2.extras import DictCursor

from src.config import Config
from src.db import LoginHistory, Role, db_models
from src.db.db_factory import init_db
from src.db.db_models import ActionType
from src.repositories.auth_repository import AuthRepository
from src.routes import attach_routes
from tests.functional.vars.roles import ROLES


@pytest.fixture(scope="session")
def test_app():
    config = Config()
    app = Flask(__name__)
    app.config.from_object(config)
    ctx = app.app_context()
    ctx.push()

    jwt = JWTManager()
    jwt.init_app(app)

    init_db(app)
    attach_routes(app)

    return app


@pytest.fixture(scope="session")
def test_db(test_app):
    db_models.db.create_all()
    db_models.db.session.commit()
    yield db_models.db


@pytest.fixture
def setup_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="session")
def test_client(test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


def clean_tables(*tables):
    DSL = {
        "dbname": current_app.config.get("POSTGRES_DB"),
        "user": current_app.config.get("POSTGRES_USER"),
        "password": current_app.config.get("POSTGRES_PASSWORD"),
        "host": current_app.config.get("POSTGRES_HOST"),
        "port": current_app.config.get("POSTGRES_PORT"),
    }

    pg_conn = psycopg2.connect(**DSL, cursor_factory=DictCursor)
    if pg_conn:
        with pg_conn.cursor() as cur:
            for table in tables:
                cur.execute("DELETE FROM %s" % table)
        pg_conn.commit()
        pg_conn.close()


@pytest.fixture
def clean_table(request):
    def teardown():
        clean_tables(*request.param)

    request.addfinalizer(teardown)


@pytest.fixture
def create_roles(test_db):
    for role_id, role_name in ROLES:
        role = Role(id=role_id, name=role_name, description="")
        test_db.session.add(role)
        test_db.session.commit()


@pytest.fixture
def create_list_user_login_history(test_db):
    email = "test77@test.ru"
    login_dt = datetime(2022, 12, 13, 14, 13, 2, 115756)
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)

    objects = [
        LoginHistory(
            user_id=user.id, created_dt=login_dt, action_type=ActionType.LOGIN.value
        )
        for _ in range(10)
    ]
    test_db.session.bulk_save_objects(objects)
    test_db.session.commit()
