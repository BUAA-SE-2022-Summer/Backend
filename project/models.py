from django.db import models
from team.models import Team


# from file.models import File


# Create your models here.
class Project(models.Model):
    projectID = models.AutoField(primary_key=True)
    projectName = models.CharField(verbose_name='项目名称', max_length=64, default='')
    projectDesc = models.TextField(verbose_name='项目描述', default='')
    projectImg = models.CharField(verbose_name='项目图片', max_length=256, default='')
    projectUser = models.IntegerField(verbose_name='项目创建者', default=0)
    projectTime = models.DateTimeField(verbose_name='项目创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_star = models.BooleanField(verbose_name='是否收藏', default=False)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    root_file = models.ForeignKey('file.File', on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='project_root')
    is_edit = models.IntegerField(verbose_name='记录编辑', default=0)
    is_sharing = models.BooleanField(default=True)
    class Meta:
        db_table = 'project'
