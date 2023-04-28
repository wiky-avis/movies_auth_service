from http import HTTPStatus

import pytest

from tests.functional.vars.auth import BAD_TOKEN, EXP_TOKEN, NO_TOKEN


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
    test_client.set_cookie(key="access_token_cookie", value=token_header)

    res = test_client.get(endpoint)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }


@pytest.mark.parametrize(
    "endpoint",
    (
        "/api/v1/users",
        "/api/v1/users/change_password",
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
    test_client.set_cookie(key="access_token_cookie", value=token_header)
    res = test_client.patch(endpoint)

    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }


@pytest.mark.parametrize(
    "endpoint",
    ("/api/v1/users",),
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
    test_client.set_cookie(key="access_token_cookie", value=token_header)

    res = test_client.delete(endpoint)
    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.json == {
        "success": False,
        "error": {"msg": "UndefinedUser."},
        "result": None,
    }
