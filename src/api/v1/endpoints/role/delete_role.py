from flask_restx import Namespace, Resource


api = Namespace(name="v1", path="/api/v1/roles")


@api.route("/delete_role")
class DeleteRole(Resource):
    def delete(self):
        pass
