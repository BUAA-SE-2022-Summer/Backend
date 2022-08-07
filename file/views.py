from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import *

from prototype.models import Prototype
from user.models import User
from project.models import Project
from team.models import Team, Team_User
from .models import File
from .error import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from prototype.views import get_prototype_list


# Create your views here.


def login_check(request):
    # return 'userID' in request.session
    lc = request.session.get('userID')
    if not lc:
        return False
    return True


def base_err_check(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()


def file_name_check(file_name, team, projectID, file_type, father_id):
    f_list = File.objects.filter(team=team,
                                 project_id=projectID,
                                 file_type=file_type,
                                 file_name=file_name,
                                 isDelete=False,
                                 fatherID=father_id)
    return len(f_list) == 0


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
    user_perm_check = Team_User.objects.filter(user=user, team=team)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法创建文件"})
    if file_type != 'dir' and file_type != 'doc' and file_type != 'uml':
        return JsonResponse({'errno': 3100, 'msg': "文件类型非法"})
    if file_name == '':
        return JsonResponse({'errno': 3099, 'msg': "文件名称不得为空"})
    if not file_name_check(file_name, team, projectID, file_type, fatherID):
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
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
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
    # base_err_check(request)
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    try:
        fileID = request.POST.get('fileID')
        content = request.POST.get('content')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    file = File.objects.get(fileID=fileID)
    file_team = file.team
    # file_pro = file.project
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法编辑"})
    if file.isDelete:
        return JsonResponse({'errno': 3093, 'msg': "文件已被删除"})
    if file.file_type == 'dir':
        return JsonResponse({'errno': 3092, 'msg': "无法编辑文件夹"})
    file.content = content
    file.save()
    file.project.is_edit = (file.project.is_edit + 1) % 2
    file.project.save()
    return JsonResponse({'errno': 0,
                         'msg': "保存成功",
                         'fileID': file.fileID,
                         'file_name': file.file_name,
                         'create_time': file.create_time,
                         'last_modify_time': file.last_modify_time,
                         'editor': user.username,
                         'file_type': file.file_type,
                         'content': file.content,
                         })


@csrf_exempt
def read_file(request):
    # base_err_check(request)
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
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
    file.project.is_edit = (file.project.is_edit + 1) % 2
    file.project.save()
    return JsonResponse({'errno': 0,
                         'msg': "打开成功",
                         'fileID': file.fileID,
                         'file_name': file.file_name,
                         'create_time': file.create_time,
                         'last_modify_time': file.last_modify_time,
                         'file_type': file.file_type,
                         'content': file.content,
                         })


def delete_dir(fileID, team, projectID):
    sub_list = File.objects.filter(fatherID=fileID, isDelete=False, team=team, project_id=projectID)
    for i in sub_list:
        if i.file_type == 'dir' and not i.isDelete:
            delete_file(i.fileID, team, projectID)
        i.isDelete = True
        i.save()


@csrf_exempt
def delete_file(request):
    # base_err_check(request)
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
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
    file_projectID = file.project_id  # Project.objects.get(projectID=file.projectID)
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法删除"})
    if file.file_type == 'dir':
        delete_dir(fileID, file_team, file_projectID)
    # 更改父节点为根目录ID
    project = Project.objects.get(projectID=file_projectID)
    project_root_file = project.root_file
    file.fatherID = project_root_file.fileID
    file.isDelete = True
    file.save()
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
    return JsonResponse({'errno': 0, 'msg': "删除成功"})


def restore_dir(fileID, team, projectID):
    try:
        file = File.objects.get(fileID=fileID, team=team, project_id=projectID, isDelete=True)
    except ObjectDoesNotExist:
        return
    sub_list = File.objects.filter(fatherID=fileID, team=team, project_id=projectID)
    for i in sub_list:
        if i.file_type == 'dir':
            restore_file(i.fileID, team, projectID)
        i.isDelete = False
        i.save()


@csrf_exempt
def restore_file(request):
    # base_err_check(request)
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    user = get_user(request)
    try:
        fileID = request.POST.get('fileID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        file = File.objects.get(fileID=fileID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3091, 'msg': "无法获取文件信息"})
    if not file.isDelete:
        return JsonResponse({'errno': 3090, 'msg': "文件不在回收站中"})
    file_team = file.team
    file_projectID = file.project_id  # Project.objects.get(projectID=file.projectID)
    user_perm_check = Team_User.objects.filter(team=file_team, user=user)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法恢复"})
    if file.file_type == 'dir':
        restore_dir(fileID, file_team, file_projectID)
    file.isDelete = False
    file.save()
    file.project.is_edit = (file.project.is_edit + 1) % 2
    file.project.save()
    return JsonResponse({'errno': 0, 'msg': "恢复成功"})


def acquire_file_list(dirID, projectID, allow_del, user, is_personal, file_type):
    res = []
    if file_type != 'pro':
        if is_personal:
            file_list = File.objects.filter(fatherID=dirID, project_id=projectID, user=user, file_type=file_type)
        else:
            file_list = File.objects.filter(fatherID=dirID, project_id=projectID, file_type=file_type)
        for i in file_list:
            if not (i.isDelete and not allow_del):
                res.append({'fileID': i.fileID,
                            'file_name': i.file_name,
                            'create_time': i.create_time,
                            'last_modify_time': i.last_modify_time,
                            'file_type': i.file_type})
        return res
    else:
        proto_list = get_prototype_list(dirID, projectID, allow_del, user, is_personal)
        return proto_list
    # proto_list = get_prototype_list(dirID, projectID, allow_del, user, is_personal)
    # res.extend(proto_list)

    # if is_personal:
    #     prototype_list = Prototype.objects.filter(fatherID=dirID, projectID=projectID)  # , prototypeUser=user)
    # else:
    #     prototype_list = Prototype.objects.filter(fatherID=dirID, projectID=projectID)
    # for j in prototype_list:
    #     if not (j.is_delete and not allow_del):
    #         # author = User.objects.get(userID=i.prototypeUser)
    #         res.append({
    #             'fileID': j.prototypeID,
    #             'file_name': j.prototypeName,
    #             'create_time': j.create_time,
    #             'last_modify_time': j.last_modify_time,
    #             'file_type': 'proto'
    #         })
    # return res


# @csrf_exempt
def project_root_filelist(request, file_type, msg):
    # base_err_check(request)
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    user = get_user(request)
    try:
        projectID = request.POST.get('projectID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        project = Project.objects.get(projectID=projectID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3089, 'msg': "无法获取项目信息"})
    # 查询用户是否处于该项目团队
    team = project.team
    user_perm_check = Team_User.objects.filter(user=user, team=team)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法查看"})
    root_file = project.root_file
    root_fileID = root_file.fileID
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
    filelist = acquire_file_list(root_fileID, projectID, False, user, False, file_type)
    return JsonResponse({'errno': 0, 'msg': '切换至' + msg + '列表', 'filelist': filelist})


@csrf_exempt
def project_root_uml_list(request):
    return project_root_filelist(request, 'uml', 'UML图')


@csrf_exempt
def project_root_doc_list(request):
    return project_root_filelist(request, 'doc', '文档')


@csrf_exempt
def project_root_pro_list(request):
    return project_root_filelist(request, 'pro', '原型图')


@csrf_exempt
def get_dir_list(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    user = get_user(request)
    try:
        dirID = request.POST.get('dirID')
        projectID = request.POST.get('projectID')
        is_personal = request.POST.get('is_personal')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        project = Project.objects.get(projectID=projectID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3089, 'msg': "无法获取项目信息"})
    # 查询用户是否处于该项目团队
    team = project.team
    user_perm_check = Team_User.objects.filter(user=user, team=team)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法查看"})
    try:
        dir = File.objects.get(fileID=dirID, isDelete=False, project_id=projectID, team=team)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3088, 'msg': "无法获取目录信息"})
    if dir.file_type != 'dir':
        return JsonResponse({'errno': 3087, 'msg': "无法展开非目录文件"})
    dir_list = acquire_file_list(dirID, projectID, False, user, is_personal, 'doc')
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
    return JsonResponse({'errno': 0, 'msg': "成功打开文件夹", 'dirlist': dir_list})


def acquire_delete_filelist(dirID, projectID):
    res = []
    sub_list = File.objects.filter(fatherID=dirID, isDelete=True, project_id=projectID)
    for i in sub_list:
        res.append({'fileID': i.fileID,
                    'file_name': i.file_name,
                    # 'create_time': i.create_time,
                    'delete_time': i.last_modify_time,
                    'file_type': i.file_type})
    return res


@csrf_exempt
def delete_filelist_in_project(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    user = get_user(request)
    try:
        projectID = request.POST.get('projectID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        project = Project.objects.get(projectID=projectID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3089, 'msg': "无法获取项目信息"})
    team = project.team
    user_perm_check = Team_User.objects.filter(user=user, team=team)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法查看"})
    root_file = project.root_file
    root_fileID = root_file.fileID
    filelist = acquire_delete_filelist(root_fileID, projectID)
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
    return JsonResponse({'errno': 0, 'msg': "成功打开回收站", 'delete_filelist': filelist})


@csrf_exempt
def get_my_filelist(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()
    user = get_user(request)
    try:
        projectID = request.POST.get('projectID')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    try:
        project = Project.objects.get(projectID=projectID)
    except ObjectDoesNotExist:
        return JsonResponse({'errno': 3089, 'msg': "无法获取项目信息"})
    team = project.team
    user_perm_check = Team_User.objects.filter(user=user, team=team)
    if len(user_perm_check) == 0:
        return JsonResponse({'errno': 3095, 'msg': "您不是该团队的成员，无法查看"})
    root_file = project.root_file
    root_fileID = root_file.fileID
    res = []
    my_file_list = File.objects.filter(fatherID=root_fileID, user=user, project_id=projectID, isDelete=False)
    for i in my_file_list:
        res.append({'fileID': i.fileID,
                    'file_name': i.file_name,
                    'create_time': i.create_time,
                    'last_modify_time': i.last_modify_time,
                    'file_type': i.file_type})
    project.is_edit = (project.is_edit + 1) % 2
    project.save()
    return JsonResponse({'errno': 0, 'msg': "成功打开我创建的文件", 'my_file_list': res})
