from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render

from backend import settings
from .error import *
# from ..myUtils.utils import *
from .models import Team, Team_User
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import *
from django.core.mail import *


# from .email import *


# Create your views here.


def login_check(request):
    # return 'userID' in request.session
    lc = request.session.get('userID')
    if not lc:
        return False
    return True


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
    Team_User.objects.create(team=new_team, user=manager, is_supervisor=True, is_creator=True)
    return JsonResponse({'errno': 0,
                         'msg': "新建团队成功",
                         'teamID': new_team.teamID,
                         'create_time': new_team.create_time,
                         'creator': manager.username})


@csrf_exempt
def invite_member(request):
    if request.method != 'POST':
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
        # team_name = request.POST.get('team_name')
        teamID = request.POST.get('teamID')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "无法获取团队id"})
    userID = request.session['userID']
    try:
        team = Team.objects.get(teamID=teamID)  # , manager=User.objects.get(userID=userID))
    except ObjectDoesNotExist:
        # return JsonResponse({'errno': 2093, 'msg': "团队不存在或您不是团队管理员，邀请失败"})
        return JsonResponse({'errno': 2093, 'msg': "团队不存在"})
    except MultipleObjectsReturned:
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    is_manager_re = Team_User.objects.filter(team=team, user=User.objects.get(userID=userID), is_supervisor=True)
    if len(is_manager_re) == 0:
        return JsonResponse({'errno': 2093, 'msg': "您不具备该团队的管理员权限"})
    relation = Team_User.objects.filter(team=team, user=target_user)
    if len(relation) != 0:
        return JsonResponse({'errno': 2091, 'msg': "您邀请的用户已在团队中"})

    send_mail(subject='来自墨书的邀请函', message='Hello, ' + target_username, from_email=settings.EMAIL_FROM,
              recipient_list=[target_user.email], html_message='<a>hello</a>')

    # new_relation = Team_User(team=team, user=target_user, is_supervisor=False, is_creator=False)
    # new_relation.save()
    return JsonResponse({'errno': 0, 'msg': "已向用户"+target_username+"发送邀请邮件"})


@csrf_exempt
def kick_member(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        teamID = request.POST.get('teamID')
        # team_name = request.POST.get('team_name')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "无法获取团队id"})
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
    try:
        user_re = Team_User.objects.get(team=team, user=user, is_supervisor=True)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "您不是团队管理员，无法踢除其他团队成员"})
    # if user != team.manager:
    #     return JsonResponse({'errno': 2093, 'msg': "您不是团队管理员，无法踢除其他团队成员"})
    try:
        kick_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2095, 'msg': "您要踢除的用户不存在"})
    # if kick_user == user:
    #     return JsonResponse({'errno': 2093, 'msg': "您不能把自己踢除团队哟～"})
    cur_relation = Team_User.objects.filter(team=team, user=kick_user)
    if len(cur_relation) == 0:
        return JsonResponse({'errno': 2091, 'msg': "无法踢除不在团队中的用户"})
    if kick_user == user:
        return JsonResponse({'errno': 2093, 'msg': "您不能把自己踢出团队哟～"})
    for i in cur_relation:
        if i.is_supervisor:
            return JsonResponse({'errno': 2087, 'msg': "您不能将管理员踢出团队"})
        i.delete()
    return JsonResponse({'errno': 0, 'msg': "踢除成功"})


@csrf_exempt
def set_manager(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        target_username = request.POST.get('username')
        teamID = request.POST.get('teamID')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "信息获取失败"})
    try:
        team = Team.objects.get(teamID=teamID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "团队不存在"})
    try:
        target_user = User.objects.get(username=target_username)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2095, 'msg': "用户不存在"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    if user != team.manager:
        return JsonResponse({'errno': 2093, 'msg': "您不具备超管权限"})
    relation = Team_User.objects.filter(team=team, user=target_user)
    if len(relation) == 0:
        return JsonResponse({'errno': 2091, 'msg': "用户不在团队中"})
    if len(relation) >= 2:
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    for r in relation:
        if r.is_supervisor:
            return JsonResponse({'errno': 2090, 'msg': "用户已是管理员"})
        r.is_supervisor = True
        r.save()
    return JsonResponse({'errno': 0, 'msg': "设置成功"})


@csrf_exempt
def delete_manager(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        target_username = request.POST.get('username')
        teamID = request.POST.get('teamID')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "信息获取失败"})
    try:
        team = Team.objects.get(teamID=teamID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "团队不存在"})
    try:
        target_user = User.objects.get(username=target_username)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2095, 'msg': "用户不存在"})
    userID = request.session['userID']  # 当前用户
    user = User.objects.get(userID=userID)
    if team.manager != user:
        return JsonResponse({'errno': 2093, 'msg': "您不具备超管权限"})
    try:
        relation = Team_User.objects.get(team=team, user=target_user, is_supervisor=True, is_creator=False)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2088, 'msg': "该用户不是普通管理员"})
    relation.is_supervisor = False
    relation.save()
    return JsonResponse({'errno': 0, 'msg': "成功解除管理权限"})


@csrf_exempt
def get_team_info(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        teamID = request.POST.get('teamID')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "信息获取失败"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        team = Team.objects.get(teamID=teamID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "团队不存在"})
    except MultipleObjectsReturned:
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    relation_check = Team_User.objects.filter(team=team, user=user)
    if len(relation_check) == 0:
        return JsonResponse({'errno': 2089, 'msg': "您不属于该团队"})
    team_user = Team_User.objects.filter(team=team)
    user_list = []
    for i in team_user:
        i_user = i.user
        user_list.append({'username': i_user.username,
                          'real_name': i_user.real_name,
                          'email': i_user.email,
                          'is_supervisor': i.is_supervisor,
                          'is_creator': i.is_creator})
    return JsonResponse({'errno': 0, 'msg': "查看成功", 'user_list': user_list})


@csrf_exempt
def rename_team(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        new_name = request.POST.get('new_name')
        teamID = request.POST.get('teamID')
    except ValueError:
        return JsonResponse({'errno': 2094, 'msg': "信息获取失败"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    team = Team.objects.get(teamID=teamID)
    try:
        relation = Team_User.objects.get(user=user, team=team, is_supervisor=True)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 2093, 'msg': "您不是该团队的管理员"})
    team_remain = Team.objects.filter(team_name=new_name)
    if len(team_remain) != 0:
        return JsonResponse({'errno': 2098, 'msg': "团队名称重复，取个新名字吧～"})
    team.team_name = new_name
    team.save()
    return JsonResponse({'errno': 0, 'msg': "修改成功"})


@csrf_exempt
def show_my_team_list(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    team_list_res = []
    team_list = Team_User.objects.filter(user=user)
    for i in team_list:
        team = i.team
        member_num_check = Team_User.objects.filter(team=team)
        num = len(member_num_check)
        team_list_res.append({
            'teamID': i.team.teamID,
            'team_name': i.team.team_name,
            'team_manager': i.team.manager.username,
            'is_creator': i.is_creator,
            'is_supervisor': i.is_supervisor,
            'member_num': num
        })
    return JsonResponse({'errno': 0, 'msg': "查看成功", 'team_list': team_list_res})
