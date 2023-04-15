from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_sign_up_temporary_user(test_client, setup_url, create_roles):
    email = "test543645@test.ru"

    res = test_client.post("/api/v1/users/sign_up", json={"email": email})
    assert res.status_code == HTTPStatus.CREATED
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
    assert body["result"]["roles"] == ["ROLE_TEMPORARY_USER"]
    assert body["result"]["verified_mail"] is False
    assert body["result"]["registered_on"]


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_sign_up_temporary_user_error_409(test_db, test_client, setup_url):
    email = "test47364@test.ru"

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)

    res = test_client.post("/api/v1/users/sign_up", json={"email": email})
    assert res.status_code == HTTPStatus.CONFLICT
    assert res.json == {
        "success": False,
        "error": {"msg": "User already exists."},
        "result": None,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_approve_user(test_db, test_client, setup_url, create_roles):
    email = "test1382493@test.ru"
    password = "MyPaSsWoRd123"

    auth_repository = AuthRepository(test_db)
    res = test_client.post("/api/v1/users/sign_up", json={"email": email})
    assert res.status_code == HTTPStatus.CREATED
    user_id = res.json["result"]["id"]

    res = test_client.patch(
        f"/api/v1/users/{user_id}/sign_up", json={"password": password}
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
    assert body["result"]["roles"] == [
        "ROLE_TEMPORARY_USER",
        "ROLE_PORTAL_USER",
    ]
    assert body["result"]["verified_mail"] is True
    assert body["result"]["registered_on"]

    user = auth_repository.get_user_by_email(email=email)
    assert user.password_hash


def test_approve_user_error_400(test_client, setup_url):
    user_id = "cfc83768-9be4-4066-be89-695d35ea9131"
    password = ""

    res = test_client.patch(
        f"/api/v1/users/{user_id}/sign_up", json={"password": password}
    )
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json
    assert body["error"]["msg"] == "User id or password is not valid."
