from flask_restx import Namespace, Resource

api = Namespace(name="Test", description="Test", path="/api/ping")


@api.route("/")
class Ping(Resource):
    def get(self):
        return "Pong"
