import uuid
from datetime import timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from src import db
from src.common.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
from src.models.role import Role


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    verified_mail = db.Column(db.Boolean, unique=False, default=False)
    login_history = db.relationship("LoginHistory", backref="user")
    roles = db.relationship(
        Role, secondary="user_role", back_populates="users"
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

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class UserRole(db.Model):
    __tablename__ = "user_role"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(User.id, ondelete="CASCADE")
    )
    role_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(Role.id, ondelete="CASCADE")
    )


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(User.id, ondelete="CASCADE")
    )
    device_type = db.Column(db.String(), primary_key=True)
    login_dt = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<LoginHistory: (User: {self.user_id}, {self.login_dt}>"
