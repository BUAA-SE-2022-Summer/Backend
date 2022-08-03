from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import *
from user.models import User
from project.models import Project
from team.models import Team
from .models import File

from .error import *


# Create your views here.


def login_check(request):
    # return 'userID' in request.session
    lc = request.session.get('userID')
    if not lc:
        return False
    return True


def file_name_check(file_name, team, project, file_type, father_id):
    list = File.objects.filter(team=team,
                               project=project,
                               file_type=file_type,
                               file_name=file_name,
                               isDelete=False,
                               father_id=father_id)
    return len(list) == 0


def get_user(request):
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    return user


@csrf_exempt
def create_file(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        teamID = request.POST.get('teamID')
        projectID = request.POST.get('projectID')
        file_name = request.POST.get('file_name')
        file_type = request.POST.get('file_type')
        fatherID = request.POST.get('fatherID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    team = Team.objects.get(teamID=teamID)
    project = Project.objects.get(projectID=projectID)
    if file_type != 'dir' and file_type != 'doc' and file_type != 'uml':
        return JsonResponse({'errno': 3100, 'msg': "文件类型非法"})
    if file_name == ' ':
        return JsonResponse({'errno': 3099, 'msg': "文件名称不得为空"})
    if not file_name_check(file_name, team, project, file_type, father_id):
        return name_duplicate_err(file_type, file_name)
    try:
        father = File.objects.get(fileID=fatherID, file_type='dir', isDelete=False, team=team, project=project)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3097, 'msg': "父文件夹不存在"})
    except MultipleObjectsReturned:
        return JsonResponse({'errno': 3096, 'msg': "父文件夹错误"})
    new_file = File(file_name=file_name,
                    file_type=file_type,
                    fatherID=fatherID,
                    isDelete=False,
                    user=user,
                    team=team,
                    project=project)
    new_file.save()
    return JsonResponse({'errno': 0,
                         'msg': "新建成功",
                         'fileID': new_file.fileID,
                         'file_name': new_file.file_name,
                         'create_time': new_file.create_time,
                         'last_modify_time': new_file.last_modify_time,
                         'author': user.username,
                         'file_type': file_type,
                         'content': new_file.content,
                         })


@csrf_exempt
def edit_file(request):
    base_err_check(request)
    try:
        fileID = request.POST.get('fileID')
        content = request.POST.get('content')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    file = File.objects.get(fileID=fileID)
    file_team = file.team
    file_pro = file.project
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法编辑"})
    if file.isDelete:
        return JsonResponse({'errno': 3093, 'msg': "文件已被删除"})
    if file.file_type == 'dir':
        return JsonResponse({'errno': 3092, 'msg': "无法编辑文件夹"})
    file.content = content
    file.save()
    return JsonResponse({'errno': 0,
                         'msg': "保存成功",
                         'fileID': file.fileID,
                         'file_name': file.file_name,
                         'create_time': file.create_time,
                         'last_modify_time': file.last_modify_time,
                         'editor': user.username,
                         'file_type': file_type,
                         'content': file.content,
                         })


@csrf_exempt
def read_file(request):
    base_err_check(request)
    try:
        fileID = request.POST.get('fileID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    user = get_user(request)
    file = File.objects.get(fileID=fileID)
    file_team = file.team
    # file_pro = file.project
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法查看"})
    if file.isDelete:
        return JsonResponse({'errno': 3093, 'msg': "文件已被删除"})
    if file.file_type == 'dir':
        return JsonResponse({'errno': 3092, 'msg': "无法查看文件夹内容"})
    return JsonResponse({'errno': 0,
                         'msg': "打开成功",
                         'fileID': file.fileID,
                         'file_name': file.file_name,
                         'create_time': file.create_time,
                         'last_modify_time': file.last_modify_time,
                         'file_type': file_type,
                         'content': file.content,
                         })


def delete_dir(fileID, team, project):
    sub_list = File.objects.filter(fatherID=fileID, isDelete=False, team=team, project=project)
    for i in sub_list:
        if i.file_type == 'dir' and not i.isDelete:
            delete_file(i.fileID, team, project)
        i.isDelete = True
        i.save()


@csrf_exempt
def delete_file(request):
    base_err_check(request)
    user = get_user(request)
    try:
        fileID = request.POST.get('fileID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        file = File.objects.get(fileID=fileID, isDelete=False)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3091, 'msg': "无法获取文件信息"})
    file_team = file.team
    file_project = file.project
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法删除"})
    if file.file_type == 'dir':
        delete_dir(fileID, team, file_project)
    # 更改父节点为根目录ID， 根目录ID待设置
    file.isDelete = True
    file.save()
    return JsonResponse({'errno': 0, 'msg': "删除成功"})


@csrf_exempt
def restore_file(request):
    base_err_check(request)
    user = get_user(request)
    try:
        fileID = request.POST.get('fileID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    