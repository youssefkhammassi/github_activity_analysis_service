from datetime import datetime
from typing import Optional, Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Query

from config.base import gaas_config, user_config
from config.injection import Container
from source.custom_exceptions import apis_exceptions
from source.schemas.user_model import User
from source.services.common_github_activity_service import CommonGithubActivityService
from source.schemas import github_activity_schema as gh_activity_schema

github_activity_router = APIRouter(

    prefix='/github-api/activity'
)


@github_activity_router.get('/{owner}/{repo}/events',
                            responses=gaas_config.responses_code,
                            response_model=gh_activity_schema.ActivityGroupOverview
                            )
@inject
async def get_events(
        owner: str = Path(...),
        repo: str = Path(...),
        offset: Optional[int] = Query(None),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> gh_activity_schema.ActivityGroupOverview:
    """
    get all repository events ( pull requests, issues, watch events )
    input:
        owner: str
        repo: str
    output: ActivityOverview
    """
    try:
        return await github_activity_service.get_events_grouped(
            owner=owner,
            repo=repo,
            offset=offset
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/pulls',
                            responses=gaas_config.responses_code,
                            response_model=gh_activity_schema.PullRequestsActivityOverview
                            )
@inject
async def get_pull_events(
        owner: str = Path(...),
        repo: str = Path(...),
        #user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> gh_activity_schema.PullRequestsActivityOverview:
    """
    get all repository pull requests events and the average time between pull requests
    input:
        owner: str
        repo: str
    output: PullRequestsActivityOverview
    """
    try:
        return await github_activity_service.get_pull_events(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/issues',
                            responses=gaas_config.responses_code,
                            response_model=gh_activity_schema.ActivityOverview)
@inject
async def get_issues_events(
        owner: str = Path(...),
        repo: str = Path(...),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> gh_activity_schema.ActivityOverview:
    """
    get all repository issues events
    input:
        owner: str
        repo: str
    output: ActivityOverview
    """
    try:
        return await github_activity_service.get_issues_events(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/watch',
                            responses=gaas_config.responses_code,
                            response_model=gh_activity_schema.ActivityOverview)
@inject
async def get_watch_events(
        owner: str = Path(...),
        repo: str = Path(...),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> gh_activity_schema.ActivityOverview:
    """
    get all repository watch events
    input:
        owner: str
        repo: str
    output: ActivityOverview
    """
    try:
        return await github_activity_service.get_watch_events(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/viz/pulls/count_per_day',
                            responses=gaas_config.responses_code,
                            response_model=dict
                            )
@inject
async def get_pull_events_count_per_day(
        owner: str = Path(...),
        repo: str = Path(...),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> dict:
    """
    get all repository count per day for pull requests events
    input:
        owner: str
        repo: str
    output: dict
    """
    try:
        return await github_activity_service.get_number_of_pull_events_per_day(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/viz/issues/count_per_day',
                            responses=gaas_config.responses_code,
                            response_model=dict
                            )
@inject
async def get_issues_events_count_per_day(
        owner: str = Path(...),
        repo: str = Path(...),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> dict:
    """
    get all repository count per day for issues events
    input:
        owner: str
        repo: str
    output: dict
    """
    try:
        return await github_activity_service.get_number_of_issues_events_per_day(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e


@github_activity_router.get('/{owner}/{repo}/events/viz/watch/count_per_day',
                            responses=gaas_config.responses_code,
                            response_model=dict
                            )
@inject
async def get_watch_events_count_per_day(
        owner: str = Path(...),
        repo: str = Path(...),
        user: User = Depends(user_config.authorize),
        github_activity_service: CommonGithubActivityService = Depends(Provide[Container.github_activity_service])
) -> dict:
    """
    get all repository count per day for watch events
    input:
        owner: str
        repo: str
    output: dict
    """
    try:
        return await github_activity_service.get_number_of_watch_events_per_day(
            owner=owner,
            repo=repo
        )
    except Exception as e:
        raise apis_exceptions.ApiNotValidGithubURL(detail=str(e)) from e
