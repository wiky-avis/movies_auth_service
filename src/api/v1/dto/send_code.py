from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


SendCodeResponse = Model.inherit(
    "SendCodeResponse",
    BaseModelResponse,
    {"result": fields.String(example="Ok")},
)
