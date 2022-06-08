import logging

from cryptography.fernet import Fernet
from dependency_injector import containers, providers

import source
from config.base import gaas_config
from source.services.github_activity_service import GithubActivityService
from source.services.github_connector import GithubApiConnector
from source.utils.fernet_encryption import fernet_decrypt

logger = logging.getLogger()


class InjectionHelper:
    pass


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[source])

    github_api_connector = providers.Factory(
        GithubApiConnector,
        access_token=fernet_decrypt(gaas_config.ENCRYPTED_GH_TOKEN, Fernet(gaas_config.ENCRYPTION_KEY)),
    )

    github_activity_service = providers.Factory(
        GithubActivityService,
        api_service=github_api_connector,
    )
