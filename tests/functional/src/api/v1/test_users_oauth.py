from http import HTTPStatus

import pytest

from src.common.collections import get_in
from tests.functional.vars.oauth import MockGoogleApi, MockYandexApi
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.parametrize(
    "provider_name",
    ("yandex", "google"),
)
def test_users_authorize(test_client, setup_url, provider_name):
    res = test_client.get(f"/api/v1/users/authorize/{provider_name}")
    assert res.status_code == HTTPStatus.FOUND


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_users_callback_yandex(
    test_db, create_roles, test_client, setup_url, monkeypatch
):
    mock_yandex_api = MockYandexApi()
    mock_yandex_api.add_mock_user_data_200(monkeypatch)
    mock_yandex_api.add_mock_user_info_200(monkeypatch)

    res = test_client.get(
        f"/api/v1/users/callback/yandex?code=1234&state=yandex"
    )
    assert res.status_code == HTTPStatus.OK

    body = res.json
    assert body.get("success") is True
    assert body.get("error") is None
    result = get_in(body, "result")
    assert result.get("id")
    assert result.get("registered_on")
    assert result.get("email") == "test@yandex.ru"
    assert result.get("roles") == ["ROLE_PORTAL_USER"]
    assert result.get("verified_mail") is False


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_users_callback_google(
    test_db, create_roles, test_client, setup_url, monkeypatch
):
    mock_google_api = MockGoogleApi()
    mock_google_api.add_mock_user_data_200(monkeypatch)
    mock_google_api.add_mock_user_info_200(monkeypatch)

    res = test_client.get(
        f"/api/v1/users/callback/google?code=1234&state=google"
    )
    assert res.status_code == HTTPStatus.OK

    body = res.json
    assert body.get("success") is True
    assert body.get("error") is None
    result = get_in(body, "result")
    assert result.get("id")
    assert result.get("registered_on")
    assert result.get("email") == "test@gmail.com"
    assert result.get("roles") == ["ROLE_PORTAL_USER"]
    assert result.get("verified_mail") is False
