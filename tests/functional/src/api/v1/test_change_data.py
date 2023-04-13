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
        json={"new_email": new_email},
        headers=headers,
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == {"success": True, "error": None, "result": "Ok"}
