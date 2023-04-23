from http import HTTPStatus

import pytest

from src.db import Role
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from tests.functional.vars.auth import TEST_PUBLIC_KEY, sign_jwt
from tests.functional.vars.roles import GET_ALL_ROLES_RESPONSE, ROLES
from tests.functional.vars.tables import CLEAN_TABLES


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
@pytest.fixture(scope="module")
def create_roles(test_db):
    for role_id, role_name in ROLES:
        role = Role(id=role_id, name=role_name, description="")
        test_db.session.add(role)
        test_db.session.commit()


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_all_roles_ok(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    email = "test6691@test.ru"
    role = RoleType.ROLE_PORTAL_ADMIN.value

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=email)
    user = auth_repository.get_user_by_email(email=email)
    roles_repository = RolesRepository(test_db)
    roles_repository.set_role_by_role_name(user=user, role_name=role)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {
        "X-Auth-Token": sign_jwt(
            str(user.id),
            roles=[
                role,
            ],
        )
    }

    res = test_client.get("/api/v1/roles", headers=headers)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == GET_ALL_ROLES_RESPONSE


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_all_roles_fail(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    user_id = "cfc83768-9be4-4066-be89-695d35ea9131"

    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {
        "X-Auth-Token": sign_jwt(
            user_id,
        )
    }

    res = test_client.get("/api/v1/roles", headers=headers)
    assert res.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_add_role(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    admin_email = "test66551@test.ru"
    admin_role = RoleType.ROLE_PORTAL_ADMIN.value

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=admin_email)
    admin_user = auth_repository.get_user_by_email(email=admin_email)
    roles_repository = RolesRepository(test_db)
    roles_repository.set_role_by_role_name(
        user=admin_user, role_name=admin_role
    )
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {
        "X-Auth-Token": sign_jwt(
            str(admin_user.id),
            roles=[
                admin_role,
            ],
        )
    }

    user_email = "test_user@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.post("/api/v1/roles", headers=headers, json=input_body)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    result = body.get("result")
    assert result["user_id"]
    assert result["roles"] == ["ROLE_PORTAL_USER"]


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_delete_role(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    admin_email = "test665541@test.ru"
    admin_role = RoleType.ROLE_PORTAL_ADMIN.value

    auth_repository = AuthRepository(test_db)
    auth_repository.create_user(email=admin_email)
    admin_user = auth_repository.get_user_by_email(email=admin_email)
    roles_repository = RolesRepository(test_db)
    roles_repository.set_role_by_role_name(
        user=admin_user, role_name=admin_role
    )
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {
        "X-Auth-Token": sign_jwt(
            str(admin_user.id),
            roles=[
                admin_role,
            ],
        )
    }

    user_email = "test_user2@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)
    roles_repository.set_role_by_id(role_id=role_portal_user, user_id=user.id)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.delete("/api/v1/roles", headers=headers, json=input_body)
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    result = body.get("result")
    assert result["user_id"]
    assert result["roles"] == []


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_check_permissions(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    role = RoleType.ROLE_PORTAL_USER.value
    user_email = "test_user@test.ru"
    auth_repository = AuthRepository(test_db)
    roles_repository = RolesRepository(test_db)
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)
    roles_repository.set_role_by_role_name(user=user, role_name=role)
    monkeypatch.setattr("src.config.Config.JWT_PUBLIC_KEY", TEST_PUBLIC_KEY)
    headers = {
        "X-Auth-Token": sign_jwt(
            str(user.id),
            roles=[
                role,
            ],
        )
    }

    res = test_client.get(
        "/api/v1/roles/check_permissions",
        headers=headers,
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    result = body.get("result")
    assert result["user_id"]
    assert result["roles"] == ["ROLE_PORTAL_USER"]
