from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_delete_account(test_db, test_client, setup_url, monkeypatch):
    email = "test66666@test.ru"
    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    payload = {"user_id": str(user.id)}
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    res = test_client.delete("/api/v1/users")
    assert res.status_code == HTTPStatus.NO_CONTENT


def test_delete_account_error_404(test_client, setup_url, monkeypatch):
    user_id = "bbbbbbbb-9be4-4066-be89-695d35ea9131"
    payload = {"user_id": str(user_id)}
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    res = test_client.delete("/api/v1/users")
    assert res.status_code == HTTPStatus.NOT_FOUND
    body = res.json
    assert body == {
        "error": {"msg": "User not found."},
        "result": None,
        "success": False,
    }
