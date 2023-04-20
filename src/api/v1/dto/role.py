from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


InputRoleModel = Model(
    "InputRoleModel",
    {
        "user_id": fields.String(required=True, description="Id пользователя"),
        "role_id": fields.String(required=True, description="Id роли"),
    },
)

OutputUserRoleModel = Model(
    "OutputUserRoleModel",
    {
        "user_id": fields.String(description="Id"),
        "roles": fields.List(fields.String(), description="Роли пользователя"),
    },
)

UserRoleResponse = Model.inherit(
    "UserRoleResponse",
    BaseModelResponse,
    {"result": fields.Nested(OutputUserRoleModel)},
)


OutputRoleModel = Model(
    "OutputRoleModel",
    {
        "role_id": fields.String(description="Id роли"),
        "name": fields.String(description="Название роли"),
    },
)

RoleResponse = Model.inherit(
    "RoleResponse",
    BaseModelResponse,
    {"result": fields.List(fields.Nested(OutputRoleModel))},
)
