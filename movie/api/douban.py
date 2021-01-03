from lxml import etree

from movie.api.async_api import AsyncApi
from movie.constants.douban_url import TOP250
from movie.decorators.auth import require_auth_async
from movie.request_models.douban import DouBanTop250GetModel
from movie.utils.http_response import json_response
from movie.utils.requests import requests


class DouBanTop250Api(AsyncApi):

    @require_auth_async
    async def get(self, request):
        body = DouBanTop250GetModel(**request.GET.dict())
        html = await requests.get(url=TOP250, params=dict(start=(body.page - 1) * 25))
        html = etree.HTML(html)
        data = html.xpath('//ol[@class="grid_view"]/li')
        result = []
        for datum in data:
            title = datum.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')
            info = datum.xpath('div/div[2]/div[@class="bd"]/p[1]/text()')
            quote = datum.xpath('div/div[2]/div[@class="bd"]/p[2]/span/text()')
            score = datum.xpath('div/div[2]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
            num = datum.xpath('div/div[2]/div[@class="bd"]/div/span[4]/text()')
            img = datum.xpath('div/div[1]/a/img/@src')
            info[0] = info[0].replace("\n                            ", "")
            info[1] = info[1].replace("\n                            ", "")
            info[1] = info[1].replace("\n                        ", "")
            result.append(dict(title=title[0], info=info, quote=quote[0], score=score[0], num=num[0], img=img[0]))

        return json_response(data=dict(top250=result, page=body.page, size=25, total=250))
