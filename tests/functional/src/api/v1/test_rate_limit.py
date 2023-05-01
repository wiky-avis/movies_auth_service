from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


email = "test44@test.ru"
password = "verygoodpassword"


@pytest.mark.usefixtures("clean_table")
@pytest.mark.usefixtures("flush_redis")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_login_with_rate_limit(
    test_db, test_client, setup_url, create_roles, redis_client
):
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)

    user = auth_repository.get_user_by_email(email=email)
    auth_repository.set_password(user=user, password=password)
    auth_repository.update_flag_verified_mail(user)

    res = test_client.post(
        "/api/v1/users/login", json={"email": email, "password": password}
    )
    assert res.status_code == HTTPStatus.OK

    for i in range(19):
        res = test_client.post(
            "/api/v1/users/login",
            json={"email": "wrong_email", "password": "wrong_password"},
        )
        assert res.status_code == HTTPStatus.NOT_FOUND

    res = test_client.post(
        "/api/v1/users/login",
        json={"email": "wrong_email", "password": "wrong_password"},
    )
    assert res.status_code == HTTPStatus.TOO_MANY_REQUESTS
