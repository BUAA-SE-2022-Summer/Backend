from django.db import models
from team.models import Team
from user.models import User


# Create your models here.
class Prototype(models.Model):
    prototypeID = models.AutoField(primary_key=True)
    prototypeName = models.CharField(verbose_name='原型名称', max_length=64, default='')
    prototypeUser = models.IntegerField(verbose_name='原型创建者', default=0)
    create_time = models.DateTimeField(verbose_name='原型创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    projectID = models.IntegerField(default=0, null=False)
    file_type = models.CharField(null=False, default='pro', max_length=100)
    fatherID = models.IntegerField(default=0)

    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    is_sharing = models.BooleanField(default=False)
    class Meta:
        db_table = 'prototype'


class Page(models.Model):
    pageID = models.AutoField(primary_key=True)
    pageName = models.CharField(verbose_name='页面名称', max_length=64, default='')
    pageComponentData = models.TextField(verbose_name='页面组件信息', default='[]')
    pageCanvasStyle = models.TextField(
        verbose_name='页面组件额外信息',
        default='{"width":1200,"height":740,"scale":100,"color":"#000","opacity":1,"background":"#fff","fontSize":14}')
    pageUser = models.IntegerField(verbose_name='页面创建者', default=0)
    pageTime = models.DateTimeField(verbose_name='页面创建时间', auto_now_add=True)
    is_first = models.BooleanField(verbose_name='是否为首页', default=False)
    prototype = models.ForeignKey(Prototype, on_delete=models.CASCADE)

    class Meta:
        db_table = 'page'


class PageUse(models.Model):
    ID = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'page_use'
