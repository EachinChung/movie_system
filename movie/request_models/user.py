import re
from enum import IntEnum

from pydantic import EmailStr, Field, validator
from pydantic.main import BaseModel


class Sex(IntEnum):
    man = 1
    women = 0


class UserBodyModel(BaseModel):
    nickname: str = Field(title="昵称")
    sex: Sex = Field(title="性别")
    email: EmailStr = Field(title="邮箱")
    password: str = Field(title="密码")

    # noinspection PyMethodParameters
    @validator("password")
    def password_validator(cls, password: str):
        """密码强度验证

        Args:
            password (str): 密码

        Raises:
            ValueError: 验证失败
        """
        if len(password) >= 6:
            return
        if re.search(r"[a-z]", password):
            return
        if re.search(r"[A-Z]", password):
            return
        if re.search(r"\d", password):
            return

        raise ValueError("value is not strong enough")
