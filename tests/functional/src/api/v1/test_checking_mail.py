from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_checking_mail(test_db, test_client, setup_url):
    email = "test@test.ru"

    res = test_client.get(f"/api/v1/users/checking_mail?email={email}")
    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json == {
        "success": False,
        "error": {"msg": "User does not exist"},
        "result": None,
    }

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    res = test_client.get(f"/api/v1/users/checking_mail?email={email}")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email


def test_checking_mail_error(test_client, setup_url):
    res = test_client.get("/api/v1/users/checking_mail")
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json == {
        "success": False,
        "error": {"msg": "Email is not valid."},
        "result": None,
    }
