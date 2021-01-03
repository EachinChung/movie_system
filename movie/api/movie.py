import json

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.views import View

from movie.api.async_api import AsyncApi
from movie.constants.douban_url import SEARCH
from movie.decorators.auth import require_auth, require_auth_async
from movie.decorators.tools import call_second_limit_async
from movie.models.comment import Comment
from movie.models.movie import Movie
from movie.request_models.movie import MovieBySearchGetModel
from movie.request_models.movie import MovieCommentGetModel
from movie.request_models.movie import MovieCommentPostModel, SearchGetModel
from movie.utils.http_response import json_response
from movie.utils.requests import requests


class SearchApi(AsyncApi):
    @require_auth_async
    @call_second_limit_async(2)
    async def get(self, request):
        """ 搜索电影 """
        body = SearchGetModel(**request.GET.dict())
        res = await requests.get(is_json=True, url=SEARCH, params=dict(q=body.q))
        return json_response(data=res)


class MovieBySearchApi(AsyncApi):
    @require_auth_async
    async def get(self, request):
        """ 通过搜索获取电影 """
        body = MovieBySearchGetModel(**request.GET.dict())
        movie = await sync_to_async(Movie.objects.get_by_name, thread_sensitive=True)(body.name)
        if movie:
            return json_response(data=movie.to_dict())

        headers = {
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        res = await requests.get(url=body.douban_url, headers=headers)
        soup = BeautifulSoup(res, "html.parser")
        soup_data = soup.select('script[type="application/ld+json"]')
        data = list(soup_data)[0]
        data = json.loads(data.string)
        movie = await sync_to_async(Movie.objects.create, thread_sensitive=True)(
            name=data['name'],
            image=data['image'],
            director=[item['name'] for item in data['director']],
            author=[item['name'] for item in data['author']],
            actor=[item['name'] for item in data['actor']],
            date_published=data['datePublished'],
            description=data['description'],
        )
        return json_response(data=movie.to_dict())


class MovieCommentApi(View):
    @require_auth
    def get(self, request, movie_id):
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
