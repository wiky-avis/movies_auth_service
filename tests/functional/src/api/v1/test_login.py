from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_login_user(test_db, test_client, setup_url, create_roles):
    email = "test44@test.ru"
    password = "123qwe"

    auth_repository = AuthRepository(test_db)
    auth_repository.create_admin(email=email, password=password)

    res = test_client.post(
        "/api/v1/users/login", json={"email": email, "password": password}
    )
    assert res.status_code == HTTPStatus.OK
    assert res.json == {
        "success": True,
        "error": None,
        "result": "Ok",
    }
