from typing import Any, NoReturn, Optional, Union

from flask_sqlalchemy import SQLAlchemy

from src.api.base.models.login_history import UserLoginHistory
from src.common.tracer import trace_request as trace
from src.db import LoginHistory, User
from src.db.db_models import SocialAccount


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    def create_user(self, email: str) -> NoReturn:
        new_user = User(email=email)
        self._db.session.add(new_user)
        self._db.session.commit()

    def create_admin(self, email: str, password: str) -> NoReturn:
        self.create_user(email=email)
        admin_user = self.get_user_by_email(email=email)
        self.set_password(user=admin_user, password=password)
        self.update_flag_verified_mail(admin_user)

    def delete_user(self, user: User) -> NoReturn:
        self._db.session.delete(user)
        self._db.session.commit()

    def set_password(self, user: User, password: str) -> NoReturn:
        user.password(password)
        self._db.session.commit()

    def set_additional_user_data(
        self,
        user: User,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
    ) -> NoReturn:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        self._db.session.commit()

    def set_email(self, user: User, email: str) -> NoReturn:
        user.email = email
        self._db.session.commit()

    @trace("get_user_by_email")
    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self._db.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        user = self._db.session.query(User).filter_by(id=user_id).first()
        return user

    def get_list_login_history(
        self, user_id: str, page: Optional[int], per_page: Optional[int]
    ) -> Union[Any, list[UserLoginHistory]]:
        login_history_data = (
            self._db.session.query(LoginHistory)
            .filter_by(user_id=user_id)
            .order_by(LoginHistory.created_dt.desc())
        ).paginate(page=page, per_page=per_page)
        login_history = [
            UserLoginHistory(
                device_type=user_history.device_type,
                login_dt=str(user_history.created_dt),
                action_type=user_history.action_type,
            )
            for user_history in login_history_data
        ]
        return login_history_data, login_history

    def update_flag_verified_mail(self, user: User) -> NoReturn:
        user.verified_mail = True
        self._db.session.commit()

    def save_action_to_login_history(
        self, user_id: str, device_type: str, user_agent: str, action_type: str
    ) -> NoReturn:
        new_action = LoginHistory(
            user_id=user_id,
            device_type=device_type,
            user_agent=user_agent,
            action_type=action_type,
        )
        self._db.session.add(new_action)
        self._db.session.commit()

    def create_social_account(
        self, social_id: str, social_name: str, user_id: str
    ) -> NoReturn:
        new_account = SocialAccount(
            social_id=social_id, social_name=social_name, user_id=user_id
        )
        self._db.session.add(new_account)
        self._db.session.commit()

    def get_social_account_by_user_id(self, user_id: str) -> Optional[User]:
        social_account = (
            self._db.session.query(SocialAccount)
            .filter_by(user_id=user_id)
            .first()
        )
        return social_account
