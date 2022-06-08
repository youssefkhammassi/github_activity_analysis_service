from .header_auth import *
from config.base import gaas_config

user_authorizer = HeaderAuth(gaas_config.ENCRYPTION_KEY)
