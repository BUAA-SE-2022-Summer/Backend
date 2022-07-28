from django.db import models


# Create your models here.
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=64, default='')
    password = models.CharField(verbose_name='密码', max_length=32, default='')
