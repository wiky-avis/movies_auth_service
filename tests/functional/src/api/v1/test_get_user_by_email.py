from http import HTTPStatus

import pytest

from src.db.db_models import Role, RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from tests.functional.vars.roles import ROLES
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.fixture(scope="module")
def create_roles(test_db):
    for _, role_name in ROLES:
        role = Role(name=role_name, description="")
        test_db.session.add(role)
        test_db.session.commit()


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_user_by_email(test_db, test_client, setup_url, create_roles):
    email = "test453@test.ru"

    res = test_client.get(f"/api/v1/users?email={email}")
    assert res.status_code == HTTPStatus.NOT_FOUND
    assert res.json == {
        "success": False,
        "error": {"msg": "User does not exist"},
        "result": None,
    }

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    roles_repository = RolesRepository(test_db)
    roles_repository.set_role_by_role_name(
        user=user, role_name=RoleType.ROLE_PORTAL_USER.value
    )
    res = test_client.get(f"/api/v1/users?email={email}")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    assert body["result"]["id"]
    assert body["result"]["email"] == email
    assert body["result"]["roles"] == [RoleType.ROLE_PORTAL_USER]
    assert body["result"]["verified_mail"] is False
    assert body["result"]["registered_on"]


def test_get_user_by_email_error_400(test_client, setup_url):
    res = test_client.get("/api/v1/users")
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json == {
        "success": False,
        "error": {"msg": "Email is not valid."},
        "result": None,
    }
