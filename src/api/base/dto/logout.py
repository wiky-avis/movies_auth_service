from flask_restx import Model, fields

from src.api.base.dto.base import BaseModelResponse


UserLogoutResponse = Model.inherit(
    "UserAuthModelResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)
