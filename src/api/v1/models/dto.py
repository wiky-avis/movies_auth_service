from flask_restx import fields, Model

base_model_response = Model(
    "BaseResponse",
    {
        "success": fields.Boolean(example=True),
        "error": fields.String(example="null"),
    },
)


InputUserRegisterModel = {
    "email": fields.String(required=True, description="Почта"),
    "password": fields.String(required=False, description="Пароль"),
}


UserModelResponse = {
    "id": fields.String(required=True, description="Id"),
    "email": fields.String(required=True, description="Почта"),
    "roles": fields.List(fields.String(), description="Роли пользователя"),
    "verified_mail": fields.Boolean(
        default=False, description="Флаг подтверждения почты"
    ),
    "registered_on": fields.String(description="Дата регистрации"),
}
