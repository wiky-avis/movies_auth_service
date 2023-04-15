from datetime import datetime
from http import HTTPStatus

import pytest

from src.config import TEST_PUBLIC_KEY
from src.db import LoginHistory
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import sign_jwt
from tests.functional.vars.login_history import USER_LOGIN_HISTORY
from tests.functional.vars.tables import CLEAN_TABLES


email = "test77@test.ru"


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.fixture(scope="module")
def create_list_user_login_history(test_db):
    login_dt = datetime(2022, 12, 13, 14, 13, 2, 115756)
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)

    objects = [
        LoginHistory(user_id=user.id, login_dt=login_dt) for _ in range(10)
    ]
    test_db.session.bulk_save_objects(objects)
    test_db.session.commit()


def test_get_list_history(
    test_db,
    test_client,
    setup_url,
    monkeypatch,
    create_list_user_login_history,
):
    auth_repository = AuthRepository(db=test_db)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.get(f"/api/v1/users/login_history", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == USER_LOGIN_HISTORY


@pytest.mark.parametrize(
    "page, per_page, pages, prev_page, next_page, has_next, has_prev, result",
    (
        (1, 3, 4, None, 2, 1, 0, 3),
        (1, 10, 1, None, None, 0, 0, 10),
        (2, 1, 10, 1, 3, 1, 1, 1),
    ),
)
def test_get_list_history_pagination(
    test_db,
    test_client,
    setup_url,
    monkeypatch,
    page,
    per_page,
    pages,
    prev_page,
    next_page,
    has_next,
    has_prev,
    result,
    create_list_user_login_history,
):
    total_count = 10
    auth_repository = AuthRepository(db=test_db)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.get(
        f"/api/v1/users/login_history?page={page}&per_page={per_page}",
        headers=headers,
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert len(body["result"]) == result
    pagination = body["pagination"]
    assert pagination["page"] == page
    assert pagination["pages"] == pages
    assert pagination["total_count"] == total_count
    assert pagination["prev_page"] == prev_page
    assert pagination["next_page"] == next_page
    assert pagination["has_next"] == has_next
    assert pagination["has_prev"] == has_prev
