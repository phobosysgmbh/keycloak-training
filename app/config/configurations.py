import logging
import os

logger = logging.getLogger(__name__)


class Config:
    NETWORK_DATA = None

    KEYCLOAK_AUDIENCE = None
    KEYCLOAK_REALM = None

    KEYCLOAK_URL = None
    KEYCLOAK_URL_EXT = None

    valid = True

    def env(
        self,
        name: str,
        required: bool = False,
        default: str | None = None,
    ) -> str | None:
        value = os.environ.get(name)
        if value is None:
            value = default

        if value is None and required:
            logger.error("%s is not configured", name)
            Config.valid = False

        return value

    def is_valid(self):
        return self.valid


def fromEnv() -> Config:
    config_data = Config()

    config_data.KEYCLOAK_AUDIENCE = config_data.env("KEYCLOAK_AUDIENCE", required=True)
    config_data.KEYCLOAK_REALM = config_data.env("KEYCLOAK_REALM", required=True)

    # Keycloak settings for internal connection
    keycloak_host = config_data.env("KEYCLOAK_HOST", required=True)
    keycloak_port = config_data.env("KEYCLOAK_PORT", required=True)
    config_data.KEYCLOAK_URL = f"http://{keycloak_host}:{keycloak_port}"

    # Keycloak settings for external connection (e.g. for the browser to get directed to keycloak)
    keycloak_host_ext = config_data.env("KEYCLOAK_HOST_EXT", required=True)
    keycloak_port_ext = config_data.env("KEYCLOAK_PORT_EXT", required=True)
    config_data.KEYCLOAK_URL_EXT = f"http://{keycloak_host_ext}:{keycloak_port_ext}"

    return config_data
