from http import HTTPStatus

import pytest
from flask import request

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_update_access_token(test_db, test_client, setup_url, create_roles):
    email = "test44@test.ru"
    password = "verygoodpassword"
    localtime = "2020-01-08T12:00:00-08:00"

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)

    user = auth_repository.get_user_by_email(email=email)
    auth_repository.set_password(user=user, password=password)
    auth_repository.update_flag_verified_mail(user)

    res = test_client.post(
        "/api/v1/users/login",
        json={"email": email, "password": password, "localtime": localtime},
    )
    assert res.status_code == HTTPStatus.OK

    res = test_client.get("/api/v1/users/login_history")
    assert res.status_code == HTTPStatus.OK

    old_access_token = request.cookies.get("access_token_cookie")
    assert old_access_token is not None

    res = test_client.post("/api/v1/users/refresh_token")
    assert res.status_code == HTTPStatus.OK

    res = test_client.get("/api/v1/users/login_history")
    assert res.status_code == HTTPStatus.OK

    new_token = request.cookies.get("access_token_cookie")
    assert new_token is not None
    assert old_access_token != new_token
