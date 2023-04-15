from flask_restx import Model, fields

from src.api.v1.dto.base import BaseModelResponse


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
