from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


SendCodeModel = Model(
    "SendCodeModel",
    {
        "code": fields.String(required=True, description="Код подтверждения"),
    },
)


SendCodeResponse = Model.inherit(
    "SendCodeResponse",
    BaseModelResponse,
    {"result": fields.Nested(SendCodeModel)},
)
