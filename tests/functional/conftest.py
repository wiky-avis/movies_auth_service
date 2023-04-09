import pytest

from src.app import create_app
from src.db.db_factory import get_db
from src.db.db_models import User


database = get_db()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture(scope="session")
def db(app, test_client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def setup_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="session")
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def user(db):
    user = User(email="test@mail.test", password="test_password")
    db.session.add(user)
    db.session.commit()
    return user
