from flask_restx import Model, fields


checking_mail_model = Model(
    "User",
    {
        "email": fields.String,
        "public_id": fields.String,
        "admin": fields.Boolean,
        "registered_on": fields.String(attribute="registered_on_str"),
        "token_expires_in": fields.String,
    },
)
