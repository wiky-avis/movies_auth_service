from flask_restx import Namespace, Resource


api = Namespace(name="v1", path="/api/v1/roles")


@api.route("/add_role")
class AddRole(Resource):
    def post(self):
        pass
