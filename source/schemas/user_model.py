from typing import List, Optional

from source.schemas.common_models import CommonModel, PyUUID


class User(CommonModel):
    id: PyUUID
    name: str
    gh_token: Optional[List[str]] = None
    email: Optional[str] = None