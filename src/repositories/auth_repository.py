from flask_sqlalchemy import SQLAlchemy

from src.api.v1.models.login_history import UserLoginHistory
from src.db import LoginHistory, Role, User, UserRole


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def find_by_email(self, email: str) -> User:
        return self.db.session.query(User).filter_by(email=email).first()

    def create_user(self, email: str) -> None:
        new_user = User(email=email)
        self.db.session.add(new_user)
        self.db.session.commit()

    def set_password(self, user: User, password: str) -> None:
        user.password(password)
        self.db.session.commit()

    def set_role(self, user: User, role_name: str) -> None:
        user_role = (
            self.db.session.query(Role).filter_by(name=role_name).first()
        )
        user.roles.append(user_role)
        self.db.session.commit()

    def get_user(self, email: str) -> User | None:
        user = self.db.session.query(User).filter_by(email=email).first()
        return user if user else None

    def get_ids_roles(self, user_id) -> list[str] | None:
        roles = self.db.session.query(UserRole).filter_by(user_id=user_id)
        roles_ids = [user_role.role_id for user_role in roles]
        return roles_ids if roles_ids else None

    def get_roles(self, roles_ids: list[str]) -> list[str]:
        roles = []
        for role_id in roles_ids:
            roles.append(
                self.db.session.query(Role).filter_by(id=role_id).first()
            )

        roles = [role.name for role in roles]
        return roles if roles else []

    def create_role(self, role_id: str, user_id: str) -> None:
        user_role = UserRole(role_id=role_id, user_id=user_id)
        self.db.session.add(user_role)
        self.db.session.commit()

    def get_list_login_history(self, user_id):
        login_history = (
            self.db.session.query(LoginHistory)
            .filter_by(user_id=user_id)
            .order_by(LoginHistory.login_dt.desc())
        )
        login_history = [
            UserLoginHistory(
                device_type=user_history.device_type,
                login_dt=str(user_history.login_dt),
            )
            for user_history in login_history
        ]
        return login_history
