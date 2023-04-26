from http import HTTPStatus

import pytest
from flask_jwt_extended import create_access_token

from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository
from tests.functional.vars.roles import GET_ALL_ROLES_RESPONSE
from tests.functional.vars.tables import CLEAN_TABLES


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
    payload = {
        "user_id": str(user.id),
        "email": email,
        "verified_mail": user.verified_mail,
        "roles": [
            role,
        ],
    }
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    res = test_client.get("/api/v1/roles")
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == GET_ALL_ROLES_RESPONSE


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_all_roles_fail(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    user_id = "cfc83768-9be4-4066-be89-695d35ea9131"
    role = RoleType.ROLE_PORTAL_USER.value
    payload = {
        "user_id": str(user_id),
        "roles": [
            role,
        ],
    }
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    res = test_client.get("/api/v1/roles")
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
    payload = {
        "user_id": str(admin_user.id),
        "email": admin_email,
        "verified_mail": admin_user.verified_mail,
        "roles": [
            admin_role,
        ],
    }
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    user_email = "test_user@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.post("/api/v1/roles", json=input_body)
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
    payload = {
        "user_id": str(admin_user.id),
        "email": admin_email,
        "verified_mail": admin_user.verified_mail,
        "roles": [
            admin_role,
        ],
    }
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )

    user_email = "test_user2@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)
    roles_repository.set_role_by_id(role_id=role_portal_user, user_id=user.id)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.delete("/api/v1/roles", json=input_body)
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
    payload = {
        "user_id": str(user.id),
        "email": user_email,
        "verified_mail": user.verified_mail,
        "roles": [
            role,
        ],
    }
    access_token = create_access_token(identity=payload)
    test_client.set_cookie(
        server_name="localhost", key="access_token_cookie", value=access_token
    )
    res = test_client.get(
        "/api/v1/roles/check_permissions",
    )

    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    result = body.get("result")
    assert result["user_id"]
    assert result["roles"] == ["ROLE_PORTAL_USER"]
