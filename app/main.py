import sys
from flask import Flask
from flask_restx import Api

from config import configurations

# Extension instances
from flask_cors import CORS
from oauth.instance import oidc

# Namespaces
from app.resources.public import ns as static_ns
from app.resources.demo import ns as demo_ns

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def create_app():
    config = load_config()

    logger.info("Starting demo server")

    app = Flask(__name__)
    app.config.from_object(config)

    load_extensions(app)
    register_namespaces(app)

    return app


def register_namespaces(app):
    resources = Api(app)

    resources.add_namespace(demo_ns)
    resources.add_namespace(static_ns)


def load_extensions(app):
    oidc.init_app(app)
    CORS(app)


def load_config():
    config = configurations.fromEnv()
    if not config.is_valid():
        logger.error("application not configured correctly")
        sys.exit(1)

    return config


def main():
    app = create_app()
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
