from abc import ABC, abstractmethod
from typing import Optional
from source.schemas import github_activity_schema as gh_activity_schema
from source.services.github_connector import GithubApiConnector


class CommonGithubActivityService(ABC):
    def __init__(self, api_service: GithubApiConnector):
        self._api = api_service

    async def get_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """get all repository events"""
        return NotImplementedError

    async def get_pull_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """get all repository pull requests events"""
        return NotImplementedError
