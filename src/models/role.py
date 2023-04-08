import uuid

from sqlalchemy.dialects.postgresql import UUID

from src import db


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
