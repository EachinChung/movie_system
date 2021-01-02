from django.contrib import admin
from django.urls import include, path

from movie.api.user import AuthApi, UserApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth', AuthApi.as_view(), name='auth'),
        path('users', UserApi.as_view(), name='user'),
    ]))
]
