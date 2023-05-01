from typing import NoReturn, Optional

from flask_sqlalchemy import SQLAlchemy

from src.api.base.models.role import RoleModel
from src.db import Role, User, UserRole


class RolesRepository:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    def set_role_by_role_name(self, user: User, role_name: str) -> NoReturn:
        role = self._db.session.query(Role).filter_by(name=role_name).first()
        user_role = UserRole(role_id=role.id, user_id=user.id)
        self._db.session.add(user_role)
        self._db.session.commit()

    def get_ids_roles_by_user_id(self, user_id) -> Optional[list[str]]:
        roles = self._db.session.query(UserRole).filter_by(user_id=user_id)
        roles_ids = [user_role.role_id for user_role in roles]
        return roles_ids

    def get_role_names_by_ids(self, roles_ids: list[str]) -> list[str]:
        roles = []
        for role_id in roles_ids:
            roles.append(
                self._db.session.query(Role).filter_by(id=role_id).first()
            )

        roles = [role.name for role in roles]
        return roles

    def get_role_names_by_role_name(self, role_name: str):
        role = self._db.session.query(Role).filter_by(name=role_name).first()
        return role

    def set_role_by_id(self, role_id: str, user_id: str) -> NoReturn:
        user_role = UserRole(role_id=role_id, user_id=user_id)
        self._db.session.add(user_role)
        self._db.session.commit()

    def create_role(self, role_name: str, description: str = "") -> NoReturn:
        new_role = Role(name=role_name, description=description)
        self._db.session.add(new_role)
        self._db.session.commit()

    def delete_role_by_id(self, role_id: str, user_id: str) -> NoReturn:
        user_role = (
            self._db.session.query(UserRole)
            .filter_by(role_id=role_id, user_id=user_id)
            .first()
        )
        self._db.session.delete(user_role)
        self._db.session.commit()

    def remove_role_by_id(self, role_id: str) -> NoReturn:
        user_role = (
            self._db.session.query(Role).filter_by(role_id=role_id).first()
        )
        self._db.session.delete(user_role)
        self._db.session.commit()

    def get_all_roles(self) -> list[RoleModel]:
        roles = self._db.session.query(Role).all()
        roles = [
            RoleModel(role_id=str(role.id), name=role.name) for role in roles
        ]
        return roles
