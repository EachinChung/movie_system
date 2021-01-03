from enum import IntEnum

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


class Size(IntEnum):
    ten = 10
    twenty = 20
    fifty = 50
    hundred = 100


class MovieCommentGetModel(BaseModel):
    page: int = Field(default=1, title="页码")
    size: Size = Field(default=10, title="每页数量")


class MovieCommentPostModel(BaseModel):
    comment: str = Field(title="评论", max_length=256)
