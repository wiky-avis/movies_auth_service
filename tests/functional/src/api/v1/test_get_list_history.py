from http import HTTPStatus

import pytest

from src.db import LoginHistory
from src.repositories.auth_repository import AuthRepository
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_list_history(test_db, test_client, setup_url):
    email = "test22@test.ru"
    auth_repository = AuthRepository(db=test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user(email=email)

    objects = [
        LoginHistory(user_id=user.id) for _ in range(10)
    ]
    test_db.session.bulk_save_objects(objects)
    test_db.session.commit()
    # email = "test22@test.ru"
    # auth_repository = AuthRepository(test_db)
    # user = auth_repository.get_user(email)
    user_id = str(user.id)
    print(user_id)
    res = test_client.get(f"/api/v1/users/{user_id}/login_history")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    print(body)
