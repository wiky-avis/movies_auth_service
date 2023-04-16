from flask_restx import Namespace, Resource


api = Namespace(name="v2", path="/api/v2/roles")


@api.route("/add_role")
class AddRole(Resource):
    def post(self):
        pass
