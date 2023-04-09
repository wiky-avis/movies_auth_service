from typing import Optional

from pydantic import BaseModel

from src.db.db_models import RoleType


class UserResponse(BaseModel):
    id: str
    email: str
    roles: Optional[list[RoleType]]
