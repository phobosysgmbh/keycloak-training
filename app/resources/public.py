import logging

from flask import send_from_directory
from flask_restx import Resource, Namespace


logger = logging.getLogger(__name__)

ns = Namespace("public", description="public static web files")


@ns.route("/<path:path>")
class StaticFiles(Resource):

    def get(self, path):
        return send_from_directory("../public", path)
