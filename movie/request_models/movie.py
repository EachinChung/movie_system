from pydantic import Field
from pydantic.main import BaseModel

from movie.constants.muster import StringEnum


class SearchGetModel(BaseModel):
    q: str = Field(title="搜索电影、电视剧、综艺、影人")


class DoubanType(StringEnum):
    movie = 'movie'


class MovieBySearchGetModel(BaseModel):
    name: str = Field(title="电影名")
    douban_url: str = Field(title="豆瓣链接")
    douban_type: DoubanType = Field(title="必须为电影类型")
