from pydantic import Field
from pydantic.main import BaseModel


class DouBanTop250ApiGetModel(BaseModel):
    page: int = Field(default=1, title="页码")
