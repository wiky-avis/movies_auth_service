from src.db import Role
from src.db.db_models import RoleType
from src.repositories.auth_repository import AuthRepository


class TestAuthRepository(AuthRepository):
    def create_role_in_bd(self):
        ls_roles = [RoleType.ROLE_TEMPORARY_USER, RoleType.ROLE_PORTAL_USER]
        for role in ls_roles:
            new_user = Role(name=role, description="")
            self.db.session.add(new_user)
            self.db.session.commit()
