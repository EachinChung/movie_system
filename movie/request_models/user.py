import re
from enum import IntEnum

from pydantic import EmailStr, Field, validator
from pydantic.main import BaseModel

from movie.constants.error_text import PASSWORD_NOT_STRONG


class Sex(IntEnum):
    man = 1
    women = 0


class UserPostModel(BaseModel):
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

        Returns:
            str: password
        """
        if len(password) < 6:
            raise ValueError(PASSWORD_NOT_STRONG)
        if not re.search(r"[a-z]", password):
            raise ValueError(PASSWORD_NOT_STRONG)
        if not re.search(r"[A-Z]", password):
            raise ValueError(PASSWORD_NOT_STRONG)
        if not re.search(r"\d", password):
            raise ValueError(PASSWORD_NOT_STRONG)

        return password


class AuthPostModel(BaseModel):
    email: EmailStr = Field(title="邮箱")
    password: str = Field(title="密码")


class AuthPutModel(BaseModel):
    refresh_token: str = Field(title="刷新token")
