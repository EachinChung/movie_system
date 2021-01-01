from typing import Union


class ApiError(Exception):
    """ api异常 """

    def __init__(self, code: str = "FFFF", message: str = '请求发生错误', data: Union[dict, list] = None):
        self.code = code
        self.message = message
        self.data = data
