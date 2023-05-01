from src.api.base.models.base import ORDJSONModelMixin
from src.common.response import BaseResponse, Pagination


class UserLoginHistory(ORDJSONModelMixin):
    device_type: str
    action_type: str
    login_dt: str


class LoginHistoryResponse(BaseResponse):
    pagination: Pagination
