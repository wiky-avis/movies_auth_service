from http import HTTPStatus

import pytest
from flask import request

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


email = "test44@test.ru"
password = "verygoodpassword"


def test_login_user(test_db, test_client, setup_url, create_roles):
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)

    user = auth_repository.get_user_by_email(email=email)
    auth_repository.set_password(user=user, password=password)
    auth_repository.update_flag_verified_mail(user)

    res = test_client.post(
        "/api/v1/users/login", json={"email": email, "password": password}
    )
    assert res.status_code == HTTPStatus.OK
    assert res.json == {
        "success": True,
        "error": None,
        "result": "Ok",
    }

    res = test_client.get("/api/v1/users/login_history")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert len(body["result"]) == 1
    assert body["result"][0]["action_type"] == "login"
    assert request.cookies.get("access_token_cookie") is not None
    assert request.cookies.get("refresh_token_cookie") is not None


@pytest.mark.usefixtures("clean_table")
@pytest.mark.usefixtures("flush_redis")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_logout_user(test_db, test_client, setup_url):
    auth_repository = AuthRepository(test_db)
    user_id = auth_repository.get_user_by_email(email=email).id

    res = test_client.delete("/api/v1/users/logout")
    assert res.status_code == HTTPStatus.NO_CONTENT

    history = auth_repository.get_list_login_history(
        user_id=user_id, page=1, per_page=10
    )
    assert history[1][1].action_type == "logout"

    res = test_client.get("/api/v1/users/login_history")
    assert res.status_code == HTTPStatus.UNAUTHORIZED

    assert request.cookies.get("access_token_cookie") == "" or None
    assert request.cookies.get("refresh_token_cookie") == "" or None
