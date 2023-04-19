from flask_sqlalchemy import SQLAlchemy

from src.api.v1.models.login_history import UserLoginHistory
from src.db import LoginHistory, User


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_user(self, email: str) -> None:
        new_user = User(email=email)
        self.db.session.add(new_user)
        self.db.session.commit()

    def delete_user(self, user: User) -> None:
        self.db.session.delete(user)
        self.db.session.commit()

    def set_password(self, user: User, password: str) -> None:
        user.password(password)
        self.db.session.commit()

    def set_email(self, user: User, email: str) -> None:
        user.email = email
        self.db.session.commit()

    def get_user_by_email(self, email: str) -> User | None:
        user = self.db.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.db.session.query(User).filter_by(id=user_id).first()
        return user

    def get_list_login_history(self, user_id, page, per_page):
        login_history_data = (
            self.db.session.query(LoginHistory)
            .filter_by(user_id=user_id)
            .order_by(LoginHistory.created_dt.desc())
        ).paginate(page=page, per_page=per_page)
        login_history = [
            UserLoginHistory(
                device_type=user_history.device_type,
                login_dt=str(user_history.created_dt),
            )
            for user_history in login_history_data
        ]
        return login_history_data, login_history

    def update_flag_verified_mail(self, user: User):
        user.verified_mail = True
        self.db.session.commit()
