from http import HTTPStatus

import pytest

from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_sign_up_temporary_user(test_db, test_client, setup_url, create_roles):
    email = "test@test.ru"

    res = test_client.post("/api/v1/users/sign_up", json={"email": email})
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
    assert body["result"]["roles"] == ["ROLE_TEMPORARY_USER"]
    assert body["result"]["verified_mail"] is False
    assert body["result"]["registered_on"]
