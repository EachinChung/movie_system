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


def sync_to_async_movies(movies):
    return json_response(data=[movie.to_dict(level="search") for movie in movies])


class SearchApi(AsyncApi):
    @call_second_limit_async(1)
    async def get(self, request):
        """ 搜索电影 """
        body = SearchGetModel(**request.GET.dict())
        res = await requests.get(is_json=True, url=SEARCH, params=dict(q=body.q))
        if res:
            return json_response(data=res)
        movies = await sync_to_async(Movie.objects.get_by_name_all, thread_sensitive=True)(body.q)
        return await sync_to_async(sync_to_async_movies)(movies)


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
        comments, total = Comment.objects.get_by_movie_id(movie_id, page=body.page,size=body.size)
        return json_response(data={
            "comments": [comment.to_dict() for comment in comments],
            "total": total
        })

    @require_auth
    def post(self, request, movie_id):
        """ 增加评论 """
        body = MovieCommentPostModel(**json.loads(request.body))
        Comment.objects.create(comment=body.comment, user_id=request.user.id, movie_id=movie_id)
        return json_response(message="评论成功")
