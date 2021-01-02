from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.db import models

from movie.constants.redis_cache_key import USER_BY_EMAIL_CACHE_KEY
from movie.constants.redis_cache_key import USER_CACHE_KEY
from movie.models.base import BaseManager


class UserManager(BaseManager):
    def _get_cache_key(self, user_id: int) -> str:
        return USER_CACHE_KEY % user_id

    def get_by_email(self, email: str):
        """通过email查询user，有60秒缓存

        Args:
            email (str): 邮箱

        Returns:
            models.Model: 数据的映射关系
        """
        key = USER_BY_EMAIL_CACHE_KEY % email
        model = cache.get(key)
        if not model:
            model = self.filter(email=email).first()
            cache.set(key, model, timeout=60)
        return model


class User(models.Model):
    SEX = (
        (0, '女'),
        (1, '男'),
    )
    objects = UserManager()
    nickname = models.CharField('昵称', max_length=30)
    sex = models.IntegerField('性别', choices=SEX)
    email = models.CharField('邮箱', max_length=128)
    password_hash = models.CharField('密码', max_length=128)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户表'

    def to_dict(self):
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'sex': self.sex,
            'email': self.email,
        }

    def delete_cache(self, *keys):
        """
        清空缓存
        :param keys: 自定义需要删除的key
        :return:
        """
        cache_keys = [
            USER_CACHE_KEY % self.id,
            USER_BY_EMAIL_CACHE_KEY % self.email,
        ]
        cache_keys.extend(keys)
        cache.delete_many(cache_keys)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        self.delete_cache()
        return ret

    def set_password(self, password: str):
        """设置密码

        Args:
            password (str): 密码
        """
        self.password_hash = make_password(password)

    def validate_password(self, password: str) -> bool:
        """校验密码是否正确

        Args:
            password (str): 密码

        Returns:
            bool: 是否正确
        """
        return check_password(self.password_hash, password)
