from django.contrib import admin

from movie.models.comment import Comment
from movie.models.movie import Movie
from movie.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'sex', 'email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date_published')


@admin.register(Comment)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'movie_id', 'comment')
