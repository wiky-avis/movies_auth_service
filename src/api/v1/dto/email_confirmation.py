from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


EmailConfirmationResponse = Model.inherit(
    "EmailConfirmationResponse",
    BaseModelResponse,
    {
        "result": fields.String(example="Ok"),
    },
)
