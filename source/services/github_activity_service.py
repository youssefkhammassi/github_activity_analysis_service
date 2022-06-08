import itertools
from datetime import timedelta, datetime, timezone
from dateutil import parser
from typing import Optional, Dict

from config.base import loop
from source.schemas import github_activity_schema as gh_activity_schema
from source.services.common_github_activity_service import CommonGithubActivityService
from source.utils.url_generator import generate_github_events_url
from source.utils.utils import average_time_between_list_datetimes, count_days_from_list_datetimes


class GithubActivityService(CommonGithubActivityService):
    async def get_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """
        get all repository events
        input:
            owner: str
            repo: str
        output: ActivityOverview
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        activity_overview = gh_activity_schema.ActivityOverview(repository=repo,
                                                                owner=owner,
                                                                activity=flatten_response)
        return activity_overview

    async def get_pull_events(self, owner: str, repo: str) -> gh_activity_schema.PullRequestsActivityOverview:
        """
        get all repository pull requests events
        input:
            owner: str
            repo: str
        output: PullRequestsActivityOverview
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = loop.run_until_complete(self._api.handle_api_response(url=url))
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_pull_request_events, list_of_dates = [], []
        for event in flatten_response:
            if event.get('type') == 'PullRequestEvent':
                event = gh_activity_schema.GithubEventCommonModel.parse_obj(event)
                list_of_pull_request_events.append(event)
                list_of_dates.append(event.created_at)
        average_between_pulls = average_time_between_list_datetimes(list_of_dates)
        pulls_activity_overview = gh_activity_schema.PullRequestsActivityOverview(
            repository=repo,
            owner=owner,
            average_duration_between_pulls=str(average_between_pulls),
            activity=list_of_pull_request_events
        )
        return pulls_activity_overview

    async def get_watch_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """
        get all repository watch events
        input:
            owner: str
            repo: str
        output: ActivityOverview
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_watch_events = [event for event in flatten_response if event.get('type') == 'WatchEvent']
        activity_overview = gh_activity_schema.ActivityOverview(repository=repo,
                                                                owner=owner,
                                                                activity=list_of_watch_events)
        return activity_overview

    async def get_issues_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        """
        get all repository issues events
        input:
            owner: str
            repo: str
        output: ActivityOverview
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_issues_events = [event for event in flatten_response if event.get('type') == 'IssuesEvent']
        activity_overview = gh_activity_schema.ActivityOverview(repository=repo,
                                                                owner=owner,
                                                                activity=list_of_issues_events)
        return activity_overview

    async def get_events_grouped(self, owner: str, repo: str,
                                 offset: Optional[int]) -> gh_activity_schema.ActivityGroupOverview:
        """
        get all repository events grouped by event types with offset
        input:
            owner: str
            repo: str
            offset: Optional[int]
        output: ActivityGroupOverview
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        activities = dict(PullRequestEvent=[], WatchEvent=[], IssuesEvent=[])
        count = 0
        for event in flatten_response:
            if event.get('type') in activities.keys() and (
                    timedelta(minutes=offset) >= datetime.now(timezone.utc) - parser.parse(
                        event.get('created_at')) if offset else True):
                activities[event.get('type')].append(event)
                count += 1
        activity_overview = gh_activity_schema.ActivityGroupOverview(repository=repo,
                                                                     owner=owner,
                                                                     activity=activities,
                                                                     count=count,
                                                                     offset=offset)
        return activity_overview

    async def get_number_of_pull_events_per_day(self, owner: str,
                                                repo: str) -> dict:
        """
        get number of pull requests events per day
        input:
            owner: str
            repo: str
        output: Dict[datetime, int]
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_dates = [parser.parse(
                        event.get('created_at')) for event in flatten_response if
                         event.get('type') == 'PullRequestEvent']
        return count_days_from_list_datetimes(list_of_dates)

    async def get_number_of_watch_events_per_day(self, owner: str,
                                                 repo: str) -> dict:
        """
        get number of watch events per day
        input:
            owner: str
            repo: str
        output: Dict[datetime, int]
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_dates = [parser.parse(
                        event.get('created_at')) for event in flatten_response if
                         event.get('type') == 'WatchEvent']
        return count_days_from_list_datetimes(list_of_dates)

    async def get_number_of_issues_events_per_day(self, owner: str,
                                                    repo: str) -> dict:
        """
        get number of issues events per day
        input:
            owner: str
            repo: str
        output: Dict[datetime, int]
        """
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        list_of_dates = [parser.parse(
                        event.get('created_at')) for event in flatten_response if
                         event.get('type') == 'IssuesEvent']
        return count_days_from_list_datetimes(list_of_dates)


