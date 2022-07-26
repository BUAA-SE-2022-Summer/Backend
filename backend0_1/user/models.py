from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=64, default= '', unique=True)
    password = models.CharField(verbose_name='密码', max_length=32, default='')
