from pydantic import Field
from pydantic.main import BaseModel


class SearchGetModel(BaseModel):
    q: str = Field(title="搜索电影、电视剧、综艺、影人")
