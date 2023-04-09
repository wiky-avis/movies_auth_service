import psycopg2
import pytest
from flask import Flask, current_app
from flask_restx import Api
from psycopg2.extras import DictCursor

from src.api.technical.ping import api as ping_api
from src.api.v1.auth.checking_mail import api as check_mail
from src.config import Config
from src.db.db_factory import db as database, init_db


@pytest.fixture(scope="session")
def test_app():
    config = Config()
    app = Flask(__name__)
    app.config.from_object(config)
    ctx = app.app_context()
    ctx.push()

    init_db(app)

    api = Api(app)
    api.add_namespace(ping_api)
    api.add_namespace(check_mail)

    return app


@pytest.fixture(scope='session')
def test_db(test_app):
    database.create_all()
    database.session.commit()
    yield database
    database.session.remove()
    database.drop_all()


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
