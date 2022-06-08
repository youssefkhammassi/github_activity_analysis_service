class NotFoundError(Exception):
    entity_name: str

    def __init__(self):
        super().__init__(f"{self.entity_name} not found")


class SourceValidationError(Exception):
    entity_name: str

    def __init__(self):
        super().__init__(f"entered data was not valid for {self.entity_name}")


class GithubActivityNotFound(NotFoundError):
    entity_name: str = "repository activity"


class NotValidGithubURL(SourceValidationError):
    entity_name: str = "Github API"
