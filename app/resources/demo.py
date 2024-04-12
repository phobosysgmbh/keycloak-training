import logging

from oauth.instance import oidc
from flask_restx import Resource, Namespace


logger = logging.getLogger(__name__)

ns = Namespace("secured", description="secured resource")


@ns.route("/test")
class TestResource(Resource):

    @oidc.check_auth("")
    def get(self):
        print("aaaaaaaaa")
        return "test"
