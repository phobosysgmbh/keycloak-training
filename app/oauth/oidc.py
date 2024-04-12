import logging

from functools import wraps

from flask import request
from keycloak.exceptions import KeycloakError
from keycloak import KeycloakOpenID

import python_jwt as jwt
import uuid

from keycloak.uma_permissions import UMAPermission as Permission

HEADER_AUTHENTICATE_BEARER = {"WWW-Authenticate": "Bearer"}

logger = logging.getLogger(__name__)


class TokenNotFoundException(Exception):
    pass


class OIDC:
    def __init__(self, app=None) -> None:
        self.kc = None
        if app:
            self.init_app(app)

    def init(self, auth_url, realm_name, client_id, client_secret=""):
        """ "initializes keycloak oidc object"""
        # secret is not mandatory for permission checks
        self.kc = KeycloakOpenID(auth_url, realm_name, client_id, client_secret)

    def init_app(self, app):
        auth_url = app.config["KEYCLOAK_URL"]
        self.init(
            auth_url, app.config["KEYCLOAK_REALM"], app.config["KEYCLOAK_AUDIENCE"]
        )

    def check_auth(self, permission: Permission = None):
        """
        A Decorator for API calls.
        """

        def wrapper(func):

            @wraps(func)
            def decorated(*args, **kwargs):
                try:
                    token = parse_keycloak_token()
                except TokenNotFoundException:
                    return "not authorized", 401, HEADER_AUTHENTICATE_BEARER

                ctx_id = str(uuid.uuid4())
                logger.info(
                    "API request - ctx_id: %s method: %s, host_url: %s, base_url: %s",
                    ctx_id,
                    request.method,
                    request.host_url,
                    request.base_url,
                )

                if self.kc is None:
                    logger.warning("%s:500, KeycloakOpenID was not initialized")
                    return "KeycloakOpenID was not initialized\n", ctx_id, 500, {}

                try:
                    username, user_id = get_user_from_token(token)
                    logger.info(
                        "%s: username: %s, userid: %s", ctx_id, username, user_id
                    )

                    logger.debug(
                        "requesting permission - ctx_id: %s, permission: %s",
                        ctx_id,
                        permission,
                    )

                    auth_status = self.kc.has_uma_access(token, permission)
                except KeycloakError as e:
                    logger.warning("%s:500, keycloak response: %s", ctx_id, e)
                    return "KC Response:\n" + str(e), 500, {}
                except Exception as e:
                    logger.warning("%s:500, internal server error: %s", ctx_id, str(e))
                    return "Internal server error:\n" + str(e), 500, {}

                if not auth_status.is_logged_in:
                    logger.warning("%s:401, not authorized", ctx_id)
                    return "not authorized", 401, HEADER_AUTHENTICATE_BEARER

                if not auth_status.is_authorized:
                    logger.warning("%s:403, forbidden", ctx_id)
                    return "forbidden", 403, HEADER_AUTHENTICATE_BEARER

                return func(*args, **kwargs)

            return decorated

        return wrapper


def get_user_from_token(token: str) -> tuple[str, str]:
    try:
        _, claims = jwt.process_jwt(token)
        username = claims.get("preferred_username")
        user_id = claims.get("sub")
    except Exception as e:
        logger.error(str(e))
        return "", ""
    return username, user_id


def parse_keycloak_token() -> str:
    token = ""
    if "Authorization" in request.headers and request.headers[
        "Authorization"
    ].startswith("Bearer "):
        token = request.headers["Authorization"].split(None, 1)[1].strip()
        logger.debug("Token from Header")
    elif "access_token" in request.form:
        token = request.form["access_token"]
        logger.debug("Token from Form")
    elif "access_token" in request.args:
        token = request.args["access_token"]
        logger.debug("Token from Args")
    else:
        raise TokenNotFoundException

    return token
