from django.core.cache import cache
from django.db import models

from movie.constants.redis_cache_key import MOVIE_CACHE_KEY
from movie.models.base import BaseManager


class MovieManager(BaseManager):
    def _get_cache_key(self, movie_id: int) -> str:
        return MOVIE_CACHE_KEY % movie_id

    def get_by_name(self, name: str):
        """通过电影名查询

        Args:
            name (str): 电影名

        Returns:
            models.Model: 数据的映射关系
        """

        model = self.filter(name__icontains=name).first()
        return model


class Movie(models.Model):
    objects = MovieManager()
    name = models.CharField('电影名称', max_length=128)
    image = models.CharField('海报', max_length=256)
    director = models.JSONField('导演')
    author = models.JSONField('编剧')
    actor = models.JSONField('演员')
    date_published = models.DateField('上映时间')
    description = models.TextField('介绍')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'movie'
        verbose_name = '电影'
        verbose_name_plural = '电影表'

    def to_dict(self):
        return {
            'movie_id': self.id,
            'name': self.name,
            'image': self.image,
            'director': self.director,
            'author': self.author,
            'actor': self.actor,
            'datePublished': self.date_published,
            'description': self.description,
        }

    def delete_cache(self, *keys):
        cache_keys = [
            MOVIE_CACHE_KEY % self.id,
        ]
        cache_keys.extend(keys)
        cache.delete_many(cache_keys)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        self.delete_cache()
        return ret
