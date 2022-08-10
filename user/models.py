from django.db import models


# Create your models here.
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='昵称', max_length=64, default='')
    password = models.TextField(verbose_name='哈希密码', default='')
    real_name = models.CharField(verbose_name='真实姓名', max_length=32, default='')
    email = models.EmailField(verbose_name='邮箱', null=True)
    phone = models.CharField(verbose_name='手机号', max_length=11, default='')
    profile = models.TextField(verbose_name='个人简介', default='')
    img = models.CharField(verbose_name='头像', max_length=256,
                           default='https://xuemolan.oss-cn-hangzhou.aliyuncs.com/default.png')

    class Meta:
        db_table = 'user'
