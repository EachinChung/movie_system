from django.db import models


class User(models.Model):
    nickname = models.CharField('昵称', max_length=30)
    sex = models.IntegerField('性别')
    email = models.CharField('邮箱', max_length=11, null=True, blank=True, db_index=True)
    password_hash = models.CharField('密码', max_length=128)
