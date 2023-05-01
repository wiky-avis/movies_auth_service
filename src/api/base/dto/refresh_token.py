from flask_restx import Model, fields

from src.api.base.dto.base import BaseModelResponse


UpdateAccessTokenResponse = Model.inherit(
    "UpdateAccessTokenResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)
