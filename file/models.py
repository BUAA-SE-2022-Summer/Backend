from django.db import models

from project.models import Project
from user.models import User
from team.models import Team


# from project.models import Project


# Create your models here.


class File(models.Model):
    fileID = models.AutoField(primary_key=True, editable=False, null=False)
    file_name = models.CharField(max_length=100)

    # projectID = models.IntegerField(default=0, null=False)
    # isDir = models.BooleanField(null=False, default=False)
    file_type = models.CharField(null=False, default='doc', max_length=100)  # 用于标记文件类型 doc为普通文档,uml为uml图,dir为文件夹

    fatherID = models.IntegerField(default=0)
    content = models.TextField(max_length=65535, null=True)
    isDelete = models.BooleanField(default=False)  # If the file has been deleted, this value is True.

    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    # last_read_time = models.DateTimeField(auto_now_add=True)  # 上次访问时间，只在read_file的时候会更新
    # user为文档的创建者
    user = models.ForeignKey(
        User,
        # to_field='userID',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # team为文档所属的团队
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    # 文档所属的项目
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True,
                                null=True)

    # team_perm = models.IntegerField(default=0)

    # # 文件互斥访问
    # # 当有人以可写权限打开此文件，其它用户就只能以只读权限打开
    # # 只读和可写两种权限的区别，在后端看只是能不能保存修改
    # using = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='using')
    # is_fav = models.BooleanField(default=False)

    class Meta:
        db_table = 'file'

    def __unicode__(self):
        return 'file_name:%s' % self.file_name

    def to_dic(self):
        return {
            'file_name': self.file_name,
            'create_time': self.create_time,
            # 'last_modify_time'
            'isDir': self.isDir,
        }
