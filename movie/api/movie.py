from html import unescape

import ujson as json
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.views import View

from movie.api.async_api import AsyncApi
from movie.constants.douban_url import SEARCH
from movie.decorators.auth import require_auth
from movie.decorators.tools import call_second_limit_async
from movie.models.comment import Comment
from movie.models.movie import Movie
from movie.request_models.movie import MovieBySearchGetModel
from movie.request_models.movie import MovieCommentGetModel
from movie.request_models.movie import MovieCommentPostModel, SearchGetModel
from movie.utils.http_response import json_response
from movie.utils.requests import requests


class SearchApi(AsyncApi):
    @call_second_limit_async(2)
    async def get(self, request):
        """ 搜索电影 """
        # body = SearchGetModel(**request.GET.dict())
        # res = await requests.get(is_json=True, url=SEARCH, params=dict(q=body.q))
        return json_response(data=[
            {
                "episode": "",
                "img": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg",
                "title": "十二怒汉",
                "url": "https://movie.douban.com/subject/1293182/?suggest=%E5%8D%81",
                "type": "movie",
                "year": "1957",
                "sub_title": "12 Angry Men",
                "id": "1293182"
            },
            {
                "episode": "",
                "img": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2242220716.jpg",
                "title": "十二公民",
                "url": "https://movie.douban.com/subject/24875534/?suggest=%E5%8D%81",
                "type": "movie",
                "year": "2014",
                "sub_title": "十二公民",
                "id": "24875534"
            },
            {
                "episode": "",
                "img": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p627041570.jpg",
                "title": "十二猴子",
                "url": "https://movie.douban.com/subject/1298744/?suggest=%E5%8D%81",
                "type": "movie",
                "year": "1995",
                "sub_title": "Twelve Monkeys",
                "id": "1298744"
            },
            {
                "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1502801739.83.jpg",
                "title": "十一月",
                "url": "https://movie.douban.com/celebrity/1378421/?suggest=%E5%8D%81",
                "sub_title": "Shiyiyue",
                "type": "celebrity",
                "id": "1378421"
            },
            {
                "img": "https://img1.doubanio.com/f/movie/ca527386eb8c4e325611e22dfcb04cc116d6b423/pics/movie/celebrity-default-small.png",
                "title": "十枝梨菜",
                "url": "https://movie.douban.com/celebrity/1358996/?suggest=%E5%8D%81",
                "sub_title": "Rina Toeda",
                "type": "celebrity",
                "id": "1358996"
            },
            {
                "img": "https://img2.doubanio.com/view/celebrity/s_ratio_celebrity/public/p10113.jpg",
                "title": "十朱幸代",
                "url": "https://movie.douban.com/celebrity/1038633/?suggest=%E5%8D%81",
                "sub_title": "Yukiyo Toake",
                "type": "celebrity",
                "id": "1038633"
            }
        ])


class MovieBySearchApi(AsyncApi):
    @staticmethod
    async def get(request):
        """ 通过搜索获取电影 """
        body = MovieBySearchGetModel(**request.GET.dict())
        movie = await sync_to_async(Movie.objects.get_by_name, thread_sensitive=True)(body.name)
        if movie:
            return json_response(data=movie.to_dict())

        res = await requests.get(url=body.douban_url)
        soup = BeautifulSoup(res, "html.parser")
        soup_data = soup.select('script[type="application/ld+json"]')
        description = soup.select('span[property="v:summary"]')
        description_tag = list(description)[0]
        description_text = str(description_tag.text).replace(" ", "")
        description_text = description_text.replace("\n", "")
        description_list = description_text.split("　　")
        data = list(soup_data)[0]
        data = json.loads(data.string)
        movie = await sync_to_async(Movie.objects.create, thread_sensitive=True)(
            name=unescape(data['name']),
            image=unescape(data['image']),
            director=[unescape(item['name']) for item in data['director']],
            author=[unescape(item['name']) for item in data['author']],
            actor=[unescape(item['name']) for item in data['actor']],
            date_published=unescape(data['datePublished']),
            douban_url=body.douban_url,
            description=description_list,
        )
        return json_response(data=movie.to_dict())


class MovieCommentApi(View):

    @staticmethod
    def get(request, movie_id):
        """ 获取评论 """
        body = MovieCommentGetModel(**request.GET.dict())
        offset = (body.page - 1) * body.size
        limit = body.size
        comments = Comment.objects.get_by_movie_id(movie_id, offset, limit)
        return json_response(data=[comment.to_dict() for comment in comments])

    @require_auth
    def post(self, request, movie_id):
        """ 增加评论 """
        body = MovieCommentPostModel(**json.loads(request.body))
        Comment.objects.create(comment=body.comment, user_id=request.user.id, movie_id=movie_id)
        return json_response(message="评论成功")
