import json
from typing import Any, Optional

from cryptography.fernet import Fernet

from config.base import gaas_config
from source.utils.logging import logger


def fernet_encrypt(object_to_encrypt: Any, fermet_tool: Fernet) -> str:
    return fermet_tool.encrypt(json.dumps(object_to_encrypt).encode()).decode()


def fernet_decrypt(object_to_decrypt: str, fermet_tool: Fernet) -> Optional[Any]:
    decrypted_user_str = fermet_tool.decrypt(object_to_decrypt.encode()).decode()
    try:
        return json.loads(decrypted_user_str)
    except Exception as exception:
        logger.exception(exception)
    return None