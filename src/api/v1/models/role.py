from src.api.v1.models.base import ORDJSONModelMixin


class RoleModel(ORDJSONModelMixin):
    role_id: str
    name: str
