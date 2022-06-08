from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict
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

    async def get_issues_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """get all repository issues events"""
        return NotImplementedError

    async def get_watch_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """get all repository watch events"""
        return NotImplementedError

    async def get_events_grouped(self, owner: str, repo: str, offset: Optional[int]) -> gh_activity_schema.ActivityOverview:
        """get all repository watch events"""
        return NotImplementedError

    async def get_number_of_pull_events_per_day(self, owner: str,
                                                repo: str) -> dict:
        """get number of pull requests events per day"""
        return NotImplementedError

    async def get_number_of_watch_events_per_day(self, owner: str,
                                                repo: str) -> dict:
        """get number of watch events per day"""
        return NotImplementedError

    async def get_number_of_issues_events_per_day(self, owner: str,
                                                repo: str) -> dict:
        """get number of issues events per day"""
        return NotImplementedError
