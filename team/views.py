from pathlib import Path

from django import http
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render
# from itsdangerous import Serializer
# from itsdangerous import Serializer
from django.template import loader

from backend import settings
from backend.settings import SECRET_KEY
from .error import *
# from ..myUtils.utils import *
from .models import Team, Team_User
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import *
from django.core.mail import *

from itsdangerous import URLSafeTimedSerializer, BadData
from django.core.mail import EmailMultiAlternatives
import os

# from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer


# from .email import *


# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent


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


def generate_verify_url(user, team, invitor):
    # serializer = Serializer(SECRET_KEY)
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    data = {'userID': user.userID, 'email': user.email, 'teamID': team.teamID, 'invitorID': invitor.userID}
    token = serializer.dumps(data).encode().decode()
    verify_url = settings.EMAIL_INVITATION_URL + '?token=' + token
    return verify_url


def generate_html_message(verify_url, username, invitor_name, team_name):
    html_message = '<p>尊敬的用户%s您好！</p>' \
                   '<p>墨书用户%s邀请您加入团队%s</p>' \
                   '<p>点击以下链接可接受邀请</p>' \
                   '<p><a href="%s">%s<a></p>' % (
                       username, invitor_name, team_name, verify_url, verify_url)  # verify_url是验证路由
    return html_message


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
    user = User.objects.get(userID=userID)

    verify_url = generate_verify_url(target_user, team, user)
    # html = generate_html_message(verify_url, target_username, user.username, team.team_name)

    context = {'invitor_name': str(user.username),
               'team_name': str(team.team_name),
               'verify_url': str(verify_url)}
    # t_path = os.path.join(BASE_DIR, 'team/../templates/invitation_format.html')
    t = loader.get_template('invitation_format.html')
    html_content = t.render(context)
    msg = EmailMultiAlternatives('来自墨书的邀请函', html_content, settings.EMAIL_FROM, [target_user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # send_mail(subject='来自墨书的邀请函', message='Hello, ' + target_username, from_email=settings.EMAIL_FROM,
    #           recipient_list=[target_user.email], html_message=html)

    # new_relation = Team_User(team=team, user=target_user, is_supervisor=False, is_creator=False)
    # new_relation.save()
    return JsonResponse({'errno': 0, 'msg': "已向用户" + target_username + "发送邀请邮件"})


def check_invitation_token(token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        userID = data.get('userID')
        email = data.get('email')
        teamID = data.get('teamID')
        invitorID = data.get('invitorID')
        try:
            user = User.objects.get(userID=userID, email=email)
            team = Team.objects.get(teamID=teamID)
            invitor = User.objects.get(userID=invitorID)
        except User.DoesNotExist:
            return None
        except Team.DoesNotExist:
            return None
        else:
            return user, team, invitor


@csrf_exempt
def confirm_invitation(request):
    if request.method != 'POST':
        method_err()
    # if login_check(request):
    #     userID = request.session['userID']
    #     cur_user = User.objects.get(userID=userID)
    token = request.POST.get('token')
    # password = request.GET.get('password')
    # accept = request.GET.get('accept')

    if not token:
        return JsonResponse({'errno': 2085, 'msg': "无法获取token信息"})
        # return http.HttpResponseBadRequest('无法获取token信息')
    user, team, invitor = check_invitation_token(token)
    if not user:
        # return http.HttpResponseBadRequest('无法获取用户信息')
        return JsonResponse({'errno': 2095, 'msg': "无法获取用户信息"})

    if not team:
        # return http.HttpResponseBadRequest('无法获取团队信息')
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    if not invitor:
        return JsonResponse({'errno': 2084, 'msg': "无法获取邀请人信息"})
    # if password != user.password:
    #     JsonResponse({'errno': 2087, 'msg': "密码错误"})
    # if not accept:
    #     html = '<p>尊敬的墨书用户%s您好！</p>' \
    #            '<p>您向墨书用户%s发出的团队邀请被拒绝</p>' % (invitor.username, user.username)
    #     send_mail(subject='来自墨书的消息', message='Hello, ' + invitor.username, from_email=settings.EMAIL_FROM,
    #               recipient_list=[invitor.email],
    #               html_message=html)
    #     JsonResponse({'errno': 0, 'msg': "您已拒绝邀请"})

    # new_relation = Team_User(team=team, user=user, is_creator=False, is_supervisor=False)
    # new_relation.save()

    return JsonResponse({'errno': 0,
                         'msg': "token解析成功",
                         'teamID': team.teamID,
                         'invitorID': invitor.userID,
                         'userID': user.userID})


@csrf_exempt
def accept_invitation(request):
    if request.method != 'POST':
        return method_err()
    # if not login_check(request):
    #     return not_login_err()
    try:
        token = request.POST.get('token')
        # password = request.POST.get('password')
    except ValueError:
        return JsonResponse({'errno': 2096, 'msg': "信息获取失败"})
    user, team, invitor = check_invitation_token(token)
    if not user:
        # return http.HttpResponseBadRequest('无法获取用户信息')
        return JsonResponse({'errno': 2095, 'msg': "无法获取用户信息"})
    if not team:
        # return http.HttpResponseBadRequest('无法获取团队信息')
        return JsonResponse({'errno': 2092, 'msg': "无法获取团队信息"})
    if not invitor:
        return JsonResponse({'errno': 2086, 'msg': "无法获取邀请者信息"})
    # if password != user.password:
    #     JsonResponse({'errno': 2087, 'msg': "密码错误"})
    re_check = Team_User.objects.filter(team=team, user=user)
    if len(re_check) != 0:
        return JsonResponse({'errno': 2084, 'msg': "您已是团队" + team.team_name + '的成员'})
    new_relation = Team_User(team=team, user=user, is_creator=False, is_supervisor=False)
    new_relation.save()
    return JsonResponse({'errno': 0, 'msg': "您已成功加入团队" + team.team_name})


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
