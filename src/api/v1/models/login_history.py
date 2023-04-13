from src.api.v1.models.base import ORDJSONModelMixin


class UserLoginHistory(ORDJSONModelMixin):
    device_type: str
    login_dt: str
