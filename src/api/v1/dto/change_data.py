from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


InputUserChangeData = Model(
    "InputUserChangeData",
    {
        "email": fields.String(description="Новая почта"),
    },
)

UserChangeDataResponse = Model.inherit(
    "UserChangeDataResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)


InputUserChangePassword = Model(
    "InputUserChangePassword",
    {
        "old_password": fields.String(description="Старый пароль"),
        "new_password": fields.String(description="Новый пароль"),
    },
)

UserChangePasswordResponse = Model.inherit(
    "UserChangePasswordResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)