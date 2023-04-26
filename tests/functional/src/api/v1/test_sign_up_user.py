from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


def test_sign_up_temporary_user(test_client, setup_url, create_roles):
    email = "test543645@test.ru"
    password = "MyPaSsWoRd123"

    res = test_client.post(
        "/api/v1/users/sign_up", json={"email": email, "password": password}
    )
    assert res.status_code == HTTPStatus.CREATED
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
    assert body["result"]["roles"] == ["ROLE_PORTAL_USER"]
    assert body["result"]["verified_mail"] is False
    assert body["result"]["registered_on"]


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_sign_up_temporary_user_error_409(test_db, test_client, setup_url):
    email = "test47364@test.ru"
    password = "MyPaSsWoRd123"

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)

    res = test_client.post(
        "/api/v1/users/sign_up", json={"email": email, "password": password}
    )
    assert res.status_code == HTTPStatus.CONFLICT
    assert res.json == {
        "success": False,
        "error": {"msg": "User already exists."},
        "result": None,
    }
