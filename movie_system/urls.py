from django.contrib import admin
from django.urls import include, path

from movie.api.douban import DouBanTop250Api
from movie.api.movie import MovieBySearchApi, MovieCommentApi, SearchApi
from movie.api.user import AuthApi, UserApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', AuthApi.as_view()),
        path('users', UserApi.as_view()),
        path('douban/', include([
            path('top250', DouBanTop250Api.as_view()),
        ])),
        path('movies/', include([
            path('', MovieBySearchApi.as_view()),
            path('search', SearchApi.as_view()),
            path('<int:movie_id>/comment', MovieCommentApi.as_view()),
        ]))
    ]))
]
