from movie.api.async_api import AsyncApi
from movie.constants.douban_url import SEARCH
from movie.decorators.auth import require_auth_async
from movie.decorators.tools import call_second_limit_async
from movie.request_models.movie import SearchGetModel
from movie.utils.http_response import json_response
from movie.utils.requests import requests


class SearchApi(AsyncApi):
    @require_auth_async
    @call_second_limit_async(3)
    async def get(self, request):
        body = SearchGetModel(**request.GET.dict())
        res = await requests.get(is_json=True, url=SEARCH, params=dict(q=body.q))
        return json_response(data=res)
