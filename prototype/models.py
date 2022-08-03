from django.db import models


# Create your models here.
class Prototype(models.Model):
    prototypeID = models.AutoField(primary_key=True)
    prototypeName = models.CharField(verbose_name='原型名称', max_length=64, default='')
    prototypeUser = models.IntegerField(verbose_name='原型创建者', default=0)
    prototypeTime = models.DateTimeField(verbose_name='原型创建时间', auto_now_add=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        db_table = 'prototype'


class Page(models.Model):
    pageID = models.AutoField(primary_key=True)
    pageName = models.CharField(verbose_name='页面名称', max_length=64, default='')
    pageComponentData = models.TextField(verbose_name='页面组件信息', default='[]')
    pageUser = models.IntegerField(verbose_name='页面创建者', default=0)
    pageTime = models.DateTimeField(verbose_name='页面创建时间', auto_now_add=True)
    is_first = models.BooleanField(verbose_name='是否为首页', default=False)
    prototype = models.ForeignKey(Prototype, on_delete=models.CASCADE)

    class Meta:
        db_table = 'page'
