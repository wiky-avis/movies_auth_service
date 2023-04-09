import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID

from src import db


class RoleType(enum.Enum):
    ROLE_TEMPORARY_USER = "ROLE_TEMPORARY_USER"
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(72), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    users = db.relationship(
        "User", secondary="default", back_populates="roles"
    )

    def __repr__(self):
        return f"<Role: {self.name}>"
