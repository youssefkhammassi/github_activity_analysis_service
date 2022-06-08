from datetime import datetime
from typing import Optional, List
from source.schemas.common_models import CommonModel, CommonModelWithExtra


class CommonGithubEntityModel(CommonModel):
    id: int
    url: str


class GithubOrgModel(CommonModelWithExtra, CommonGithubEntityModel):
    login: str
    gravatar_id: str
    avatar_url: str


class GithubActorModel(CommonModelWithExtra, CommonGithubEntityModel):
    login: str
    gravatar_id: str
    avatar_url: str


class GithubRepoModel(CommonModelWithExtra, CommonGithubEntityModel):
    name: str


class GithubEventCommonModel(CommonModelWithExtra):
    type: str
    public: bool
    payload: dict
    repo: GithubRepoModel
    actor: GithubActorModel
    org: Optional[GithubOrgModel]
    created_at: datetime
    id: int


class ActivityOverview(CommonModel):
    repository: str
    owner: str
    organization: Optional[str]
    activity: List[GithubEventCommonModel]


class GithubActivityTypesModel(CommonModel):
    PullRequestEvent: List[GithubEventCommonModel]
    IssuesEvent: List[GithubEventCommonModel]
    WatchEvent: List[GithubEventCommonModel]


class ActivityGroupOverview(ActivityOverview):
    count: int
    activity: GithubActivityTypesModel
    offset: Optional[int]


class PullRequestsActivityOverview(CommonModel):
    average_duration_between_pulls: str
    repository: str
    owner: str
    organization: Optional[str]
    activity: List[GithubEventCommonModel]
