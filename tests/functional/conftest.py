import pytest

from src import create_app


@pytest.fixture
def setup_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
