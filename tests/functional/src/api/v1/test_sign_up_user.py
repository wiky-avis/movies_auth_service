from http import HTTPStatus

import pytest

from src.db import Role
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.roles import ROLES
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.fixture(scope="module")
def create_roles(test_db):
    for role in ROLES:
        role = Role(name=role, description="")
        test_db.session.add(role)
        test_db.session.commit()


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
