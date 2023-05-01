from src.api.base.models.base import ORDJSONModelMixin


class RoleModel(ORDJSONModelMixin):
    role_id: str
    name: str
