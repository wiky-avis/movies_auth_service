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
