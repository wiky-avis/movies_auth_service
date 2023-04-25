from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


UserLogoutResponse = Model.inherit(
    "UserAuthModelResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)
