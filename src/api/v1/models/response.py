from typing import List, Optional

from src.api.v1.models.base import IdModelMixin, ORDJSONModelMixin
from src.common.response import BaseResponse, Pagination
from src.db.db_models import RoleType


class UserResponse(IdModelMixin, ORDJSONModelMixin):
    email: str
    roles: List[RoleType] = list()
    verified_mail: Optional[bool] = None
    registered_on: Optional[str] = None


class LoginHistoryResponse(BaseResponse):
    pagination: Pagination


class DeleteAccountResponse(ORDJSONModelMixin):
    user_id: str
    deleted: bool
