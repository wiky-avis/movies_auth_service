from flask_restx import Namespace, Resource


api = Namespace(name="default", path="/api/ping")


@api.route("")
class Ping(Resource):
    def get(self):
        return "Pong"
