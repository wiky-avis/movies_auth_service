from typing import Any, NoReturn, Union

from flask_sqlalchemy import SQLAlchemy

from src.api.v1.models.login_history import UserLoginHistory
from src.db import LoginHistory, User


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_user(self, email: str) -> NoReturn:
        new_user = User(email=email)
        self.db.session.add(new_user)
        self.db.session.commit()

    def create_admin(self, email: str, password: str) -> NoReturn:
        self.create_user(email=email)
        admin_user = self.get_user_by_email(email=email)
        self.set_password(user=admin_user, password=password)
        self.update_flag_verified_mail(admin_user)

    def delete_user(self, user: User) -> NoReturn:
        self.db.session.delete(user)
        self.db.session.commit()

    def set_password(self, user: User, password: str) -> NoReturn:
        user.password(password)
        self.db.session.commit()

    def set_email(self, user: User, email: str) -> NoReturn:
        user.email = email
        self.db.session.commit()

    def get_user_by_email(self, email: str) -> User | None:
        user = self.db.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.db.session.query(User).filter_by(id=user_id).first()
        return user

    def get_list_login_history(
        self, user_id: str, page: int, per_page: int
    ) -> Union[Any, list[UserLoginHistory]]:
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

    def update_flag_verified_mail(self, user: User) -> NoReturn:
        user.verified_mail = True
        self.db.session.commit()

    def save_action_to_login_history(
        self, user_id, device_type, user_agent, action_type
    ):
        new_action = LoginHistory(
            user_id=user_id,
            device_type=device_type,
            user_agent=user_agent,
            action_type=action_type,
        )
        self.db.session.add(new_action)
        self.db.session.commit()
