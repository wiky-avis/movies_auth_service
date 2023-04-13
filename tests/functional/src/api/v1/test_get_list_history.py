from http import HTTPStatus

import pytest

from src.config import TEST_PUBLIC_KEY
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.auth import BAD_TOKEN, EXP_TOKEN, NO_TOKEN, sign_jwt
from tests.functional.vars.login_history import USER_LOGIN_HISTORY
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_list_history(
    test_db,
    test_client,
    setup_url,
    create_list_user_login_history,
    monkeypatch,
):
    email = "test22@test.ru"
    auth_repository = AuthRepository(db=test_db)
    user = auth_repository.get_user_by_email(email=email)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": sign_jwt(str(user.id))}

    res = test_client.get(f"/api/v1/users/login_history", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == USER_LOGIN_HISTORY


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
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
    create_list_user_login_history,
    monkeypatch,
    page,
    per_page,
    pages,
    prev_page,
    next_page,
    has_next,
    has_prev,
    result,
):
    email = "test22@test.ru"
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


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.mark.parametrize(
    "token_header",
    [NO_TOKEN, BAD_TOKEN, EXP_TOKEN],
)
def test_get_list_history_undefined_user(
    test_db,
    test_client,
    setup_url,
    create_list_user_login_history,
    monkeypatch,
    token_header,
):
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": token_header}

    res = test_client.get(f"/api/v1/users/login_history", headers=headers)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }
