import logging
from http import HTTPStatus

from src.api.v1.models.response import UserRoleResponse
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
        self.auth_repository = auth_repository
        self.roles_repository = roles_repository

    def get_user_roles(self, user_id: str) -> list[str]:
        roles_ids = self.roles_repository.get_ids_roles_by_user_id(user_id)
        roles = self.roles_repository.get_role_names_by_ids(roles_ids)
        return roles

    def get_all_roles(self):
        roles = self.roles_repository.get_all_roles()
        return BaseResponse(success=True, result=roles).dict(), HTTPStatus.OK

    def check_permissions(self, user_id: str):
        if not user_id:
            logger.error("user_id is not valid: %s", user_id, exc_info=True)
            return (
                BaseResponse(
                    success=False, error={"msg": "user_id is not valid."}
                ).dict(),
                HTTPStatus.BAD_REQUEST,
            )
        user = self.auth_repository.get_user_by_id(user_id)
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
        user = self.auth_repository.get_user_by_id(user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self.roles_repository.set_role_by_id(user_id=user_id, role_id=role_id)

        user_roles = self.get_user_roles(user_id)
        user = UserRoleResponse(
            user_id=user_id,
            roles=user_roles,
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK

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
        user = self.auth_repository.get_user_by_id(user_id)
        if not user:
            return (
                BaseResponse(
                    success=False, error={"msg": "User does not exist"}
                ).dict(),
                HTTPStatus.NOT_FOUND,
            )

        self.roles_repository.delete_role_by_id(
            user_id=user_id, role_id=role_id
        )

        user_roles = self.get_user_roles(user_id)
        user = UserRoleResponse(
            user_id=user_id,
            roles=user_roles,
        )
        return BaseResponse(success=True, result=user).dict(), HTTPStatus.OK
