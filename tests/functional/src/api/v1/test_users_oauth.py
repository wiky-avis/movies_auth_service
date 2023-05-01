from http import HTTPStatus

import pytest

from tests.functional.vars.oauth import MockYandexApi, MockGoogleApi
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
def test_users_callback_yandex(test_db, test_client, setup_url, monkeypatch):
    mock_yandex_api = MockYandexApi()
    mock_yandex_api.add_mock_user_data_200(monkeypatch)
    mock_yandex_api.add_mock_user_info_200(monkeypatch)

    res = test_client.get(f"/api/v1/users/callback/yandex?code=1234")
    assert res.status_code == HTTPStatus.OK


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_users_callback_google(test_db, test_client, setup_url, monkeypatch):
    mock_google_api = MockGoogleApi()
    mock_google_api.add_mock_user_data_200(monkeypatch)
    mock_google_api.add_mock_user_info_200(monkeypatch)

    res = test_client.get(f"/api/v1/users/callback/google?code=1234")
    assert res.status_code == HTTPStatus.OK
