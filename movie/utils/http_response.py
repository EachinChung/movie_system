from typing import Union

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def json_response(code: str = "0000", message: str = 'ok', data: Union[dict, list] = None) -> JsonResponse:
    """对齐API的json返回格式，确保至少包含code、msg、data三个字段

    Args:
        code (str, optional): code. Defaults to 0.
        message (str, optional): msg. Defaults to 'ok'.
        data (Union[dict, list], optional): data. Defaults to None.

    Returns:
        JsonResponse: Response
    """
    if data is None:
        data = {}
    return JsonResponse({'code': code, 'message': message, 'data': data})


# 限制请求方法
require_get = require_http_methods(("GET",))
require_post = require_http_methods(("POST",))
require_put = require_http_methods(("PUT",))
require_patch = require_http_methods(("PATCH",))
require_delete = require_http_methods(("DELETE",))
