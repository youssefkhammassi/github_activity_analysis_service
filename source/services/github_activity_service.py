import itertools

from config.base import loop
from source.schemas import github_activity_schema as gh_activity_schema
from source.services.common_github_activity_service import CommonGithubActivityService
from source.utils.url_generator import generate_github_events_url
from source.utils.utils import average_time_between_list_datetimes


class GithubActivityService(CommonGithubActivityService):
    async def get_events(self, owner: str, repo: str) -> gh_activity_schema.ActivityOverview:
        url = generate_github_events_url(owner=owner, repo=repo)
        response = await self._api.handle_api_response(url=url)
        flatten_response = list(itertools.chain.from_iterable(response))
        activity_overview = gh_activity_schema.ActivityOverview(repository=repo,
                                                                owner=owner,
                                                                activity=flatten_response)
        return activity_overview

    async def get_pull_events(self, owner: str, repo: str) -> gh_activity_schema.PullRequestsActivityOverview:
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
