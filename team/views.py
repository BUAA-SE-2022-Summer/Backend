from django.shortcuts import render
from .error import *
# from ..myUtils.utils import *
from .models import Team, Team_User
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import *


# Create your views here.


def login_check(request):
    return 'userID' in request.session


@csrf_exempt
def create_team(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    userID = request.session['userID']
    try:
        team_name = request.POST.get('team_name')
    except ValueError:
        return JsonResponse({'errno': 2100, 'msg': "请输入团队名称"})
    if len(team_name) == 0:
        return JsonResponse({'errno': 2099, 'msg': "团队名称不能为空"})
    manager = User.objects.get(userID=userID)
    name_check_list = Team.objects.filter(team_name=team_name)
    if len(name_check_list) != 0:
        return JsonResponse({'errno': 2098, 'msg': "团队名称重复，取个新名字吧～"})
    new_team = Team(manager=manager, team_name=team_name)
    new_team.save()
    Team_User.objects.create(team=new_team, user=manager, is_supervisor=True)
    return JsonResponse({'errno': 0,
                         'msg': "新建团队成功",
                         'teamID': new_team.teamID,
                         'create_time': new_team.create_time})


@csrf_exempt
def invite_member(request):
    if requet.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        target_username = request.POST.get('username')
        target_user = User.objects.get(username=target_username)
    except ValueError:
        return JsonResponse({'errno': 2096, 'msg': "信息获取失败"})
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2095, 'msg': "您邀请的用户不存在"})
    try:
        team_name = request.POST.get('team_name')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "无法获取团队名称"})
    userID = request.session['userID']
    try:
        team = Team.objects.get(team_name=team_name, manager=User.objects.get(userID=userID))
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "团队不存在或您不是团队管理员，邀请失败"})
    except MultipleObjectsReturned:
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})

    relation = Team_User.objects.filter(team=team, user=target_user)
    if len(relation) != 0:
        return JsonResponse({'errno': 2091, 'msg': "您邀请的用户已在团队中"})

    new_relation = Team_User(team=team, user=target_user, is_supervisor=False)
    new_relation.save()
    return JsonResponse({'errno': 0, 'msg': "邀请成功"})


@csrf_exempt
def kick_member(request):
    if requet.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        teamID = request.POST.get('teamID')
        # team_name = request.POST.get('team_name')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "无法获取团队名称"})
    try:
        username = request.POST.get('username')
    except ValueError:
        return JsonResponse({'errno': 2096, 'msg': "成员信息获取失败"})
    # # # ###########==================================================================
    # team_list = Team.objects.filter(manager=user)  # 获取以当前用户为管理员的所有团队
    # if len(team_list) == 0:
    #     return JsonResponse({'errno': 2093, 'msg': "您不是团队管理员，无法踢除其他团队成员"})
    # flag = False
    # for i in team_list:
    #     if i.team_name == team_name:
    #         flag = True
    #         break
    # if not flag:
    #     return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    # # # ###########==================================================================
    try:
        team = Team.objects.get(teamID=teamID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "团队不存在"})
    except MultipleObjectsReturned:
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    if user != team.manager:
        return JsonResponse({'errno': 2093, 'msg': "您不是团队管理员，无法踢除其他团队成员"})
    try:
        kick_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2095, 'msg': "用户不存在"})

    cur_relation = Team_User.objects.filter(team=team, user=kick_user)
    if len(cur_relation) == 0:
        return JsonResponse({'errno': 2091, 'msg': "无法踢除不在团队中的用户"})
    for i in cur_relation:
        i.delete()
    return JsonResponse({'errno': 0, 'msg': "踢除成功"})
