from flask_sqlalchemy import SQLAlchemy

from src.db import Role, User, UserRole


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.session.query(User).filter_by(email=email).first()

    def create_user(self, email: str):
        new_user = User(email=email)
        self.db.session.add(new_user)
        self.db.session.commit()

    def set_password(self, user: User, password: str):
        user.password(password)
        self.db.session.commit()

    def set_role(self, user, role_name):
        user_role = (
            self.db.session.query(Role).filter_by(name=role_name).first()
        )
        user.roles.append(user_role)
        self.db.session.commit()

    def get_user(self, email: str):
        user = self.db.session.query(User).filter_by(email=email).first()
        return user if user else None

    def get_ids_roles(self, user_id):
        roles = self.db.session.query(UserRole).filter_by(user_id=user_id)
        roles_ids = [user_role.role_id for user_role in roles]
        return roles_ids if roles_ids else None

    def get_roles(self, roles_ids):
        roles = []
        for role_id in roles_ids:
            roles.append(
                self.db.session.query(Role).filter_by(id=role_id).first()
            )

        roles = [role.name for role in roles]
        return roles if roles else []

    def create_role(self, role_id: str, user_id: str):
        user_role = UserRole(role_id=role_id, user_id=user_id)
        self.db.session.add(user_role)
        self.db.session.commit()
