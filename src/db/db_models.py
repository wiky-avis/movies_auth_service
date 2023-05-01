import enum
import uuid
from datetime import timezone

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash

from src.common.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)


db = SQLAlchemy()


class BaseMixin:
    def to_dict(self):
        return {
            c.name: getattr(self, c.name, None) for c in self.__table__.columns
        }


class UUIDMixin(BaseMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class RoleType(str, enum.Enum):
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"


class Role(UUIDMixin, db.Model):
    __tablename__ = "roles"

    name = db.Column(db.String(72), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship(
        "User", secondary="user_role", back_populates="roles"
    )

    def __repr__(self):
        return f"<Role: {self.name}>"


class User(UUIDMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    registered_on = db.Column(db.DateTime, default=utc_now)
    verified_mail = db.Column(db.Boolean, unique=False, default=False)
    login_history = db.relationship("LoginHistory", backref="user")
    roles = db.relationship(
        "Role", secondary="user_role", back_populates="users"
    )
    social_accounts = db.relationship(
        "SocialAccount",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<User email={self.email}>"

    @hybrid_property
    def registered_on_str(self):
        registered_on_utc = make_tzaware(
            self.registered_on, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(
            registered_on_utc, use_tz=get_local_utcoffset()
        )

    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        self.password_hash = generate_password_hash(
            password=password, salt_length=log_rounds
        )


class UserRole(UUIDMixin, db.Model):
    __tablename__ = "user_role"

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(User.id, ondelete="CASCADE")
    )
    role_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(Role.id, ondelete="CASCADE")
    )


class DeviceType(str, enum.Enum):
    WEB = "web"
    MOBILE = "mobile"
    TABLET = "tablet"
    UNKNOWN = "unknown"


class ActionType(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class LoginHistory(UUIDMixin, db.Model):
    __tablename__ = "login_history"

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(User.id, ondelete="CASCADE")
    )
    action_type = db.Column(db.String)
    device_type = db.Column(
        db.String,
        nullable=False,
        default=DeviceType.WEB.value,
    )
    user_agent = db.Column(db.Text)
    created_dt = db.Column(db.DateTime, nullable=False, default=utc_now)

    def __repr__(self):
        return f"<LoginHistory: (User: {self.user_id}, {self.created_dt}>"


class SocialAccount(UUIDMixin, db.Model):
    __tablename__ = "social_account"

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
    )
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("social_id", "social_name", name="social_pk"),
    )

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
