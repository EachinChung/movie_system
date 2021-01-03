from django.contrib import admin

from movie.models.movie import Movie
from movie.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'sex', 'email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date_published')
