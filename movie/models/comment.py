from django.core.cache import cache
from django.db import models

from movie.constants.redis_cache_key import COMMENT_CACHE_KEY
from movie.models.base import BaseManager
from movie.utils.tools import datetime2str


class CommentManager(BaseManager):
    def _get_cache_key(self, comment_id: int) -> str:
        return COMMENT_CACHE_KEY % comment_id

    def get_by_movie_id(self, movie_id, offset, limit):
        return self.filter(movie_id=movie_id)[offset: limit]


class Comment(models.Model):
    objects = CommentManager()
    comment = models.CharField('评论', max_length=256)
    user_id = models.IntegerField('用户id')
    movie_id = models.IntegerField('电影id')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论表'

    def to_dict(self):
        return {
            'comment_id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'comment': self.comment,
            'create_time': datetime2str(self.create_time),
            'update_time': datetime2str(self.update_time),
        }

    def delete_cache(self, *keys):
        cache_keys = [
            COMMENT_CACHE_KEY % self.id,
        ]
        cache_keys.extend(keys)
        cache.delete_many(cache_keys)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        self.delete_cache()
        return ret
