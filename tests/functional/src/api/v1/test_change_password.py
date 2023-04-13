from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import TEST_PUBLIC_KEY, sign_jwt
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_change_password(test_db, test_client, setup_url, monkeypatch):
    email = "test66@test.ru"
    old_password = "abraabra"
    new_password = "abracadabra"
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    auth_repository.set_password(user, old_password)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.put("/api/v1/users/change_password", json={"old_password": old_password, "new_password": new_password}, headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    print(body)
