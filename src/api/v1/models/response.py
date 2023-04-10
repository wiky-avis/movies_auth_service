from datetime import datetime
from typing import List, Optional

from src.api.v1.models.base import ORDJSONModelMixin
from src.db.db_models import RoleType


class UserResponse(ORDJSONModelMixin):
    email: str
    roles: List[RoleType]
    verified_mail: Optional[bool]
    registered_on: Optional[datetime]
