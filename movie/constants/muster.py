from enum import Enum


class StringEnum(str, Enum):
    pass


class Method(StringEnum):
    get = "get"
    post = "post"
    put = 'put'
    patch = 'patch'
    delete = 'delete'
