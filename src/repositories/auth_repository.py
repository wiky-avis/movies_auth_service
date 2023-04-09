from flask_sqlalchemy import SQLAlchemy
from src.db import User


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def find_by_email(self, email):
        return self.db.session.query(User).filter_by(email=email).first()

    def create_user(self, email: str, password: str):
        new_user = User()
        new_user.email = email
        new_user.password = password
        self.db.session.add(new_user)
        self.db.session.commit()
