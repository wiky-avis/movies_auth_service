from flask_restx import Model, fields


BaseModelResponse = Model(
    "BaseResponse",
    {
        "success": fields.Boolean(example=True),
        "error": fields.String(example="null"),
    },
)

ErrorModel = Model(
    "ErrorModel",
    {
        "msg": fields.String,
    },
)

ErrorModelResponse = Model(
    "ErrorModelResponse",
    {
        "success": fields.Boolean(example=False),
        "error": fields.Nested(ErrorModel),
    },
)

DeleteAccountModel = Model(
    "DeleteAccountModel",
    {
        "user_id": fields.String(),
        "deleted": fields.Boolean(example=True),
    },
)

DeleteAccountResponse = Model.inherit(
    "DeleteAccountResponse",
    BaseModelResponse,
    {"result": fields.Nested(DeleteAccountModel)},
)


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

EmailConfirmationResponse = Model.inherit(
    "EmailConfirmationResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)


LoginHistoryModel = Model(
    "LoginHistoryModel",
    {
        "device_type": fields.String(),
        "login_dt": fields.DateTime(),
    },
)

PaginationModel = Model(
    "PaginationModel",
    {
        "has_next": fields.Integer(default=0),
        "has_prev": fields.Integer(default=0),
        "next_page": fields.Integer(default=None),
        "page": fields.Integer(default=1),
        "pages": fields.Integer(default=1),
        "prev_page": fields.Integer(default=None),
        "total_count": fields.Integer(default=1),
    },
)


LoginHistoryResponse = Model.inherit(
    "LoginHistoryResponse",
    BaseModelResponse,
    {
        "result": fields.List(fields.Nested(LoginHistoryModel)),
        "pagination": fields.Nested(PaginationModel),
    },
)
