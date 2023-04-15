from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


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
