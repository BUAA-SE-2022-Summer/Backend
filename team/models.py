import os
import sys

# os.chdir(os.path.dirname(__file__))
# sys.path.append("..")
from django.db import models
from user.models import User


# Create your models here.


class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE
    )
    recently_used = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team'


class Team_User(models.Model):
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE,
    )
    is_supervisor = models.BooleanField(null=False, default=False)
    is_creator = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = 'team_user'
