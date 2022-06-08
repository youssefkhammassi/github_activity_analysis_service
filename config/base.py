import asyncio
from logging.config import dictConfig
import nest_asyncio
from cached_property import cached_property
from pydantic import BaseSettings
from config import app_config_mapping_env, gh_token
from source.utils.logging import LogConfig


class GithubActivityAnalysisServiceConfig(BaseSettings):
    HOST = app_config_mapping_env["host"]
    PORT = int(app_config_mapping_env["port"])
    ENCRYPTION_KEY = app_config_mapping_env["encryption_key"]
    ENCRYPTED_GH_TOKEN = gh_token

    # Database information

    responses_code = {
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        401: {"description": "Authentication information is missing or invalid"},
        400: {"description": "Bad request"}
    }


gaas_config = GithubActivityAnalysisServiceConfig() #gaas: Github Activity Analysis service


class UserConfig:
    @cached_property
    def authorize(self):
        from source.utils.auth import HeaderAuth
        return HeaderAuth(gaas_config.ENCRYPTION_KEY).auth()


user_config = UserConfig()
loop = asyncio.get_event_loop()

nest_asyncio.apply()