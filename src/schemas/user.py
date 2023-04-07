import uuid

from sqlalchemy.dialects.postgresql import UUID

from src import database as db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    users = db.relationship(
        "User", secondary="default", back_populates="roles"
    )

    def __repr__(self):
        return f"<Role: {self.name}>"


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
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    login_history = db.relationship("LoginHistory", backref="user")

    def __repr__(self):
        return f"<User {self.login}>"


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
        return f"<LoginHistory: (User: {self.user_id}, {self.datetime}>"


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
