from http import HTTPStatus

import pytest

from src.db.redis import redis_client
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_email_confirmation(test_db, test_client, setup_url):
    email = "test10101@test.ru"
    secret_code = 709888
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    redis_client.set(name=str(user.id), value=secret_code, ex=10)

    res = test_client.post(f"/api/v1/users/{user.id}/mail?code={secret_code}")
    assert res.status_code == HTTPStatus.OK
    assert res.json == {"error": None, "result": "Ok", "success": True}
    assert user.verified_mail is True


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_email_confirmation_error_404(test_db, test_client, setup_url):
    email = "test20101@test.ru"
    secret_code = 70900
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)

    res = test_client.post(f"/api/v1/users/{user.id}/mail?code={secret_code}")
    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json == {"error": None, "result": None, "success": False}
