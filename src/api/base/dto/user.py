from flask_restx import Model, fields

from src.api.base.dto.base import BaseModelResponse


InputUserRegisterModel = Model(
    "InputUserRegister",
    {
        "email": fields.String(required=True, description="Почта"),
        "password": fields.String(required=True, description="Пароль"),
        "localtime": fields.String(
            required=True, description="Локальное время пользователя"
        ),
    },
)

BaseUserModel = Model(
    "BaseUserModel",
    {
        "id": fields.String(required=True, description="Id"),
        "email": fields.String(required=True, description="Почта"),
        "roles": fields.List(fields.String(), description="Роли пользователя"),
        "registered_on": fields.String(description="Дата регистрации"),
        "tz": fields.String(description="Временная зона"),
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


ConfirmMailModel = Model(
    "ConfirmMailModel",
    {
        "code": fields.String(required=True, description="Код подтверждения"),
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


InputUserAuthModel = Model.inherit(
    "InputUserAuthModel",
    InputUserRegisterModel,
)

UserAuthModelResponse = Model.inherit(
    "UserAuthModelResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)
