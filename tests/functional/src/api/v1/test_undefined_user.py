from http import HTTPStatus

import pytest

from tests.functional.vars.auth import (
    BAD_TOKEN,
    EXP_TOKEN,
    NO_TOKEN,
    TEST_PUBLIC_KEY,
)


@pytest.mark.parametrize(
    "endpoint",
    ("/api/v1/users/login_history",),
)
@pytest.mark.parametrize(
    "token_header",
    (NO_TOKEN, BAD_TOKEN, EXP_TOKEN),
)
def test_undefined_user_method_get(
    test_db,
    test_client,
    setup_url,
    monkeypatch,
    endpoint,
    token_header,
):
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": token_header}

    res = test_client.get(endpoint, headers=headers)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }


@pytest.mark.parametrize(
    "endpoint",
    (
        "/api/v1/users/change_data",
        "/api/v1/users/change_password",
        "/api/v1/users/change_password",
        "/api/v1/users/change_data",
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


@pytest.mark.parametrize(
    "endpoint",
    ("/api/v1/users/delete_account",),
)
@pytest.mark.parametrize(
    "token_header",
    (NO_TOKEN, BAD_TOKEN, EXP_TOKEN),
)
def test_undefined_user_method_delete(
    test_db,
    test_client,
    setup_url,
    monkeypatch,
    token_header,
    endpoint,
):
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {"X-Auth-Token": token_header}

    res = test_client.delete(endpoint, headers=headers)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }
