from http import HTTPStatus

import pytest

from src import settings
from src.common.collections import get_in
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
    res = test_client.get(
        "/api/srv/roles", headers={"X-TOKEN": settings.TEST_TOKEN}
    )
    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body == GET_ALL_ROLES_RESPONSE


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_get_add_role(
    create_roles, test_db, test_client, setup_url, monkeypatch
):
    auth_repository = AuthRepository(test_db)

    user_email = "test_user@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.post(
        "/api/srv/roles",
        json=input_body,
        headers={"X-TOKEN": settings.TEST_TOKEN},
    )
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
    auth_repository = AuthRepository(test_db)
    user_email = "test_user2@test.ru"
    role_portal_user = "5eff1f88-8f2b-40c5-a4d0-85893cb7071b"
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)
    roles_repository = RolesRepository(test_db)
    roles_repository.set_role_by_id(role_id=role_portal_user, user_id=user.id)

    input_body = {"user_id": str(user.id), "role_id": role_portal_user}
    res = test_client.delete(
        "/api/srv/roles",
        json=input_body,
        headers={"X-TOKEN": settings.TEST_TOKEN},
    )
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
    auth_repository = AuthRepository(test_db)
    role = RoleType.ROLE_PORTAL_USER.value
    user_email = "test_user@test.ru"
    roles_repository = RolesRepository(test_db)
    auth_repository.create_user(email=user_email)
    user = auth_repository.get_user_by_email(email=user_email)
    roles_repository.set_role_by_role_name(user=user, role_name=role)

    res = test_client.get(
        f"/api/srv/roles/check_permissions?user_id={str(user.id)}",
        headers={"X-TOKEN": settings.TEST_TOKEN},
    )

    assert res.status_code == HTTPStatus.OK
    body = res.json
    assert body["success"] is True
    result = body.get("result")
    assert result["user_id"]
    assert result["roles"] == ["ROLE_PORTAL_USER"]


def test_create_role_ok(test_db, test_client, setup_url, monkeypatch):
    new_role = "ROLE_SUBSCRIBER"
    input_body = {"role_name": new_role}
    res = test_client.post(
        "/api/srv/roles/create_role",
        json=input_body,
        headers={"X-TOKEN": settings.TEST_TOKEN},
    )
    assert res.status_code == HTTPStatus.CREATED
    body = res.json
    assert body.get("error") is None
    assert body.get("success") is True
    assert get_in(body, "result", "role_id")
    assert get_in(body, "result", "name") == new_role


@pytest.mark.usefixtures("clean_table")
@pytest.mark.parametrize("clean_table", [CLEAN_TABLES], indirect=True)
def test_delete_role_ok(test_db, test_client, setup_url, monkeypatch):
    role_name = "ROLE_SUBSCRIBER"
    roles_repository = RolesRepository(test_db)
    role = roles_repository.get_role_names_by_role_name(role_name)
    res = test_client.delete(
        f"/api/srv/roles/{str(role.id)}/delete_role",
        headers={"X-TOKEN": settings.TEST_TOKEN},
    )
    assert res.status_code == HTTPStatus.NO_CONTENT
