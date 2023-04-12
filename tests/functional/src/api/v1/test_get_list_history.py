from http import HTTPStatus

import pytest

from src.config import TEST_PUBLIC_KEY
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import sign_jwt
from tests.functional.vars.login_history import USER_LOGIN_HISTORY
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_list_history(
    test_db, test_client, setup_url, create_list_user_login_history, monkeypatch
):
    email = "test22@test.ru"
    auth_repository = AuthRepository(db=test_db)
    user = auth_repository.get_user(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.get(f"/api/v1/users/{user.id}/login_history", headers=headers)
    assert res.status_code == HTTPStatus.OK
    assert res.json == USER_LOGIN_HISTORY
