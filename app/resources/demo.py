import logging
from datetime import datetime

from oauth.instance import oidc
from flask_restx import Resource, Namespace


logger = logging.getLogger(__name__)

ns = Namespace("secured", description="secured resource")


@ns.route("/test")
class TestResource(Resource):

    @oidc.check_auth("")
    def get(self):
        return f"test performed: {datetime.now()}"


@ns.route("/test2")
class TestResource2(Resource):

    @oidc.check_auth("candidates#view")
    def get(self):
        return f"test performed with 'view-candidates' role: {datetime.now()}"
