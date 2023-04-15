from flask_restx import Namespace, Resource


api = Namespace(name="v2", path="/api/v2/roles")


@api.route("/checking_rights")
class CheckingRights(Resource):
    def get(self):
        pass
