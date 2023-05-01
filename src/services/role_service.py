import logging
from http import HTTPStatus
from typing import Optional

from src.api.base.models.role import RoleModel
from src.api.base.models.user import UserRoleResponse
from src.common.response import BaseResponse
from src.repositories.auth_repository import AuthRepository
from src.repositories.role_repository import RolesRepository


logger = logging.getLogger(__name__)


class RolesService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        roles_repository: RolesRepository,
    ):
        self._auth_repository = auth_repository
        self._roles_repository = roles_repository

    def get_user_roles(self, user_id: str) -> list[str]:
        roles_ids = self._roles_repository.get_ids_roles_by_user_id(user_id)
        roles = self._roles_repository.get_role_names_by_ids(roles_ids)
        return roles

    def get_all_roles(self):
        roles = self._roles_repository.get_all_roles()
        return BaseResponse(success=True, result=roles).dict(), HTTPStatus.OK

    def check_permissions(self, user_id: str):
        user = self._auth_repository.get_user_by_id(user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )
        user_roles = self.get_user_roles(user_id)
        user = UserRoleResponse(
            user_id=user_id,
            roles=user_roles,
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

    def add_role(self, user_id: str, role_id: str):
        if not user_id or not role_id:
            logger.error(
                "invalid user_id or role_id: user_id %s role_id %s",
                user_id,
                role_id,
                exc_info=True,
            )
            return (
                BaseResponse(
                    success=False, error={"msg": "Invalid user_id or role_id."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self._auth_repository.get_user_by_id(user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self._roles_repository.set_role_by_id(user_id=user_id, role_id=role_id)

        user_roles = self.get_user_roles(user_id)
        user = UserRoleResponse(
            user_id=user_id,
            roles=user_roles,
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

    def create_role(self, role_name: str, description: Optional[str]):
        if not role_name:
            return (
                BaseResponse(
                    success=False, error={"msg": "Did not pass role_name."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        self._roles_repository.create_role(
            role_name=role_name, description=description
        )

        role = self._roles_repository.get_role_names_by_role_name(
            role_name=role_name
        )
        new_role = RoleModel(
            role_id=role.id,
            name=role.name,
        )
        return (
            BaseResponse(success=True, result=new_role).dict(),
            HTTPStatus.OK,
        )

    def delete_role(self, user_id: str, role_id: str):
        if not user_id or not role_id:
            logger.error(
                "invalid user_id or role_id: user_id %s role_id %s",
                user_id,
                role_id,
                exc_info=True,
            )
            return (
                BaseResponse(
                    success=False, error={"msg": "Invalid user_id or role_id."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self._auth_repository.get_user_by_id(user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self._roles_repository.delete_role_by_id(
            user_id=user_id, role_id=role_id
        )

        user_roles = self.get_user_roles(user_id)
        user = UserRoleResponse(
            user_id=user_id,
            roles=user_roles,
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

    def remove_role(self, role_id: str):
        if not role_id:
            return (
                BaseResponse(
                    success=False, error={"msg": "Did not pass role_id."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )

        self._roles_repository.remove_role_by_id(role_id=role_id)
        return BaseResponse(success=True).dict(), HTTPStatus.NO_CONTENT
