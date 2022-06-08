import json

from cryptography.fernet import Fernet
from fastapi import Header, HTTPException
from typing import Optional

from pydantic import ValidationError
from starlette.requests import Request

from source.utils.logging import logger
from source.schemas.user_model import User
from source.utils.fernet_encryption import fernet_encrypt, fernet_decrypt


class HeaderAuth:
    def __init__(self, encryption_key):
        self.encryption_key = encryption_key

    def auth(self):
        return AuthHandler(self.encryption_key)


class AuthHandler:
    def __init__(self, encryption_key):
        self.encryption_key = encryption_key
        self.fermet_tool = Fernet(self.encryption_key)

    def _get_user(self, user=None) -> Optional[User]:
        if not user:
            return None

        user_dict = self.decrypt_user_info(user)

        try:
            user_model = User.parse_obj(user_dict)
        except ValidationError as e:
            logger.error(f'Error due to: {e}')
            return None
        return user_model

    def __call__(self, request: Request, user: str = Header(...)) -> User:

        active_user = self._get_user(user)
        if active_user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return active_user

    def encrypt_user_info(self, user: dict) -> str:
        return fernet_encrypt(object_to_encrypt=user, fermet_tool=self.fermet_tool)

    def decrypt_user_info(self, encrypted_user: str) -> Optional[dict]:
        return fernet_decrypt(object_to_decrypt=encrypted_user, fermet_tool=self.fermet_tool)
