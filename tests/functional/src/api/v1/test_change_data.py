from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import TEST_PUBLIC_KEY, sign_jwt
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_change_data(test_db, test_client, setup_url, monkeypatch):
    email = "test44@test.ru"
    new_email = "test55@test.ru"
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.put(
        "/api/v1/users/change_data",
        json={"email": new_email},
        headers=headers,
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == {"success": True, "error": None, "result": "Ok"}


def test_change_data_error_404(test_client, setup_url, monkeypatch):
    user_id = "bbbbbbbb-9be4-4066-be89-695d35ea9131"
    new_email = "test55@test.ru"
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user_id))}

    res = test_client.put(
        "/api/v1/users/change_data",
        json={"email": new_email},
        headers=headers,
    )
    assert res.status_code == HTTPStatus.NOT_FOUND
    body = res.json
    assert body == {
        "success": False,
        "error": {"msg": "User does not exist"},
        "result": None,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_change_data_error_400(test_db, test_client, setup_url, monkeypatch):
    email = "test88@test.ru"
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.put(
        "/api/v1/users/change_data",
        json={"email": ""},
        headers=headers,
    )
    assert res.status_code == HTTPStatus.BAD_REQUEST
    body = res.json
    assert body == {
        "success": False,
        "error": {"msg": "No new email."},
        "result": None,
    }


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_change_data_error_409(test_db, test_client, setup_url, monkeypatch):
    email = "test99@test.ru"
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.put(
        "/api/v1/users/change_data",
        json={"email": email},
        headers=headers,
    )
    assert res.status_code == HTTPStatus.CONFLICT
    body = res.json
    assert body == {
        "success": False,
        "error": {"msg": "User with this email already exists."},
        "result": None,
    }
