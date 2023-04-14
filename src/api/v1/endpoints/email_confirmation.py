from http import HTTPStatus

from flask_restx import Namespace, Resource, fields, reqparse
from src.db.db_factory import db
from src.db.redis import redis_client
from src.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService

api = Namespace(name="v1", path="/api/v1/users")
parser = reqparse.RequestParser()
parser.add_argument("code", type=str)


email_confirmation_model_response = api.model(
    "EmailConfirmationResponse",
    {
        "result": fields.String(example="Ok"),
    },
)


@api.route("/<string:user_id>/mail")
class EmailConfirmation(Resource):
    @api.doc(
        responses={
            int(HTTPStatus.OK): (
                "Email confirmed.",
                email_confirmation_model_response,
            ),
        },
        description="Подтверждение почты.",
    )
    @api.param("code", "Код подтверждения почты")
    def put(self, user_id):
        args = parser.parse_args()
        code = args.get("code")
        auth_repository = AuthRepository(db)
        auth_service = AuthService(repository=auth_repository)

        print(redis_client.ping())
        redis_client.set(user_id, code)

        code = redis_client.get(user_id)
        print("---CODE", code)

        return "Ok"
