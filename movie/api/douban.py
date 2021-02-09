import ujson as json
from django.core.cache import cache
from lxml import etree

from movie.api.async_api import AsyncApi
from movie.constants.douban_url import TOP250
from movie.request_models.douban import DouBanTop250GetModel
from movie.utils.http_response import json_response
from movie.utils.requests import requests


class DouBanTop250Api(AsyncApi):

    @staticmethod
    async def get(request):
        """ 豆瓣top250 """
        body = DouBanTop250GetModel(**request.GET.dict())
        cakey = f"DouBan:Top250:{body.page}"
        result = cache.get(cakey)
        if result:
            return json_response(data=json.loads(result))

        data = await DouBanTop250Api.get_douban_top_250(body)
        cache.set(cakey, json.dumps(data), timeout=3600)
        return json_response(data=data)

    # noinspection SpellCheckingInspection
    @staticmethod
    async def get_douban_top_250(body):
        res = await requests.get(url=TOP250, params=dict(start=(body.page - 1) * 25))
        html = etree.HTML(res)
        data = html.xpath('//ol[@class="grid_view"]/li')
        movie_list = []
        for datum in data:
            url = datum.xpath('div/div[2]/div[@class="hd"]/a/@href')
            title = datum.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')
            info = datum.xpath('div/div[2]/div[@class="bd"]/p[1]/text()')
            quote = datum.xpath('div/div[2]/div[@class="bd"]/p[2]/span/text()')
            score = datum.xpath('div/div[2]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
            num = datum.xpath('div/div[2]/div[@class="bd"]/div/span[4]/text()')
            img = datum.xpath('div/div[1]/a/img/@src')
            info[0] = info[0].replace("\n                            ", "")
            info[1] = info[1].replace("\n                            ", "")
            info[1] = info[1].replace("\n                        ", "")
            movie_list.append(
                {
                    'url': url[0],
                    'title': title[0],
                    'info': info,
                    'quote': quote[0],
                    'score': score[0],
                    'num': num[0],
                    'img': img[0]
                }
            )

        return {'top250': movie_list, 'page': body.page, 'size': 25, 'total': 250}
