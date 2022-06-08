import urllib.parse
from abc import ABC


class DatabaseDetails(ABC):
    def __init__(self, host: str, user: str, pwd: str, port: str, db_name: str, schema: str):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.schema = schema
        self.db_name = db_name

    def get_url(self):
        return NotImplementedError


class PGDatabaseDetails(DatabaseDetails):

    def __init__(self, host: str, user: str, pwd: str, port: str, db_name: str, schema: str = "postgresql"):
        super().__init__(host, user, pwd, port, db_name, schema)

    def get_url(self) -> str:
        return f"{self.schema}://{self.host}:{self.port}/{self.db_name}?user={urllib.parse.quote(self.user)}&password={urllib.parse.quote(self.pwd)}"


class MySqlDatabaseDetails(DatabaseDetails):

    def __init__(self, host: str, user: str, pwd: str, port: str, db_name: str, schema: str = "mysql"):
        super().__init__(host, user, pwd, port, db_name, schema)

    def get_url(self) -> str:
        return f"{self.schema}://{self.host}:{self.port}/{self.db_name}?user={urllib.parse.quote(self.user)}&password={urllib.parse.quote(self.pwd)}"
