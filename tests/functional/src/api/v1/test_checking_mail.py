from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_checking_mail(test_db, test_client, setup_url):
    email = "test@test.ru"
    password = "pass"

    res = test_client.get(f"/api/v1/users/checking_mail?email={email}")
    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json == {
        "success": False,
        "error": {"msg": "User does not exist"},
        "result": None,
    }

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email, password=password)
    res = test_client.get(f"/api/v1/users/checking_mail?email={email}")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
