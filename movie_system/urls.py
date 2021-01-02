from django.contrib import admin
from django.urls import include, path

from movie.api.douban import DouBanTop250Api
from movie.api.user import AuthApi, UserApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', AuthApi.as_view(), name='auth'),
        path('users', UserApi.as_view(), name='user'),
        path('douban/', include([
            path('top250', DouBanTop250Api.as_view(), name='dou_ban_top250'),
        ]))
    ]))
]
