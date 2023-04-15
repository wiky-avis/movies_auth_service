from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


InputUserRegisterModel = Model(
    "InputUserRegister",
    {
        "email": fields.String(required=True, description="Почта"),
        "password": fields.String(required=False, description="Пароль"),
    },
)

BaseUserModel = Model(
    "BaseUserModel",
    {
        "id": fields.String(required=True, description="Id"),
        "email": fields.String(required=True, description="Почта"),
        "roles": fields.List(fields.String(), description="Роли пользователя"),
        "registered_on": fields.String(description="Дата регистрации"),
    },
)

RegisteredUserModel = Model.inherit(
    "RegisteredUserModel",
    BaseUserModel,
    {
        "verified_mail": fields.Boolean(
            default=True, description="Флаг подтверждения почты"
        ),
    },
)

TemporaryUserModel = Model.inherit(
    "TemporaryUserModel",
    BaseUserModel,
    {
        "verified_mail": fields.Boolean(
            default=False, description="Флаг подтверждения почты"
        ),
    },
)


RegisteredUserModelResponse = Model.inherit(
    "RegisteredUserModelResponse",
    BaseModelResponse,
    {"result": fields.Nested(RegisteredUserModel)},
)

TemporaryUserModelResponse = Model.inherit(
    "TemporaryUserModelResponse",
    BaseModelResponse,
    {"result": fields.Nested(TemporaryUserModel)},
)
