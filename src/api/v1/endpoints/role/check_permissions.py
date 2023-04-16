from flask_restx import Namespace, Resource


api = Namespace(name="v1", path="/api/v1/roles")


@api.route("/checking_rights")
class CheckingRights(Resource):
    def get(self):
        pass
