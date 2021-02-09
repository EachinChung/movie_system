from pydantic import Field
from pydantic.main import BaseModel


class DouBanTop250GetModel(BaseModel):
    page: int = Field(default=1, title="页码")
