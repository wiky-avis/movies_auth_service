from datetime import datetime
from http import HTTPStatus

import pytest

from src.db import LoginHistory
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import (
    BAD_TOKEN,
    EXP_TOKEN,
    NO_TOKEN,
    TEST_PUBLIC_KEY,
)
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.fixture(scope="module")
def create_list_user_login_history(test_db):
    email = "test77@test.ru"
    login_dt = datetime(2022, 12, 13, 14, 13, 2, 115756)
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)

    objects = [
        LoginHistory(user_id=user.id, login_dt=login_dt) for _ in range(10)
    ]
    test_db.session.bulk_save_objects(objects)
    test_db.session.commit()


@pytest.mark.parametrize(
    "endpoint",
    (
        "/api/v1/users/change_data",
        "/api/v1/users/change_password",
        "/api/v1/users/login_history",
    ),
)
@pytest.mark.parametrize(
    "token_header",
    (NO_TOKEN, BAD_TOKEN, EXP_TOKEN),
)
def test_undefined_user_method_put(
    test_db,
    test_client,
    setup_url,
    monkeypatch,
    token_header,
    endpoint,
):
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": token_header}

    res = test_client.put(endpoint, headers=headers)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }
