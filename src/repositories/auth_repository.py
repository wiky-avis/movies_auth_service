from flask_sqlalchemy import SQLAlchemy

from src.db import Role, User, UserRole


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def find_by_email(self, email):
        return self.db.session.query(User).filter_by(email=email).first()

    def create_user(self, **kwargs):
        new_user = User(**kwargs)
        self.db.session.add(new_user)
        self.db.session.commit()

    def get_user(self, email):
        user = self.db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        return user

    def get_role(self, name: str):
        role = self.db.session.query(Role).filter_by(name=name).first()
        return role.id if role else None

    def create_role(self, email, role_name):
        user = self.get_user(email)
        role_id = self.get_role(role_name)
        if not user or not role_id:
            return None
        if role_id:
            user_role = UserRole(role_id=role_id, user_id=user.id)
            self.db.session.add(user_role)
            self.db.session.commit()
