from http import HTTPStatus

import pytest

from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.usefixtures("flush_redis")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_send_code(test_db, test_client, setup_url, redis_client):
    email = "test10101@test.ru"
    code = "12345"
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    redis_client.set(name=str(user.id), value=code, ex=10)
    redis_code = redis_client.get(name=str(user.id))

    res = test_client.post(f"/api/v1/users/{user.id}/send_code")
    assert res.status_code == HTTPStatus.OK
    assert code == redis_code
    assert res.json == {"success": True, "error": None, "result": "Ok"}
