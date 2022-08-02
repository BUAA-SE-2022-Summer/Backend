from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import *
from user.models import User
from .error import *


# Create your views here.


def login_check(request):
    # return 'userID' in request.session
    lc = request.session.get('userID')
    if not lc:
        return False
    return True


def file_name_check(file_name, user, team):
    list = File.objects.filter


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
        father_id = request.POST.get('father_id')
    except ValueError:
        return JsonResponse({'errno': 3094, 'msg': "信息获取失败"})
    team = Team.objects.get(teamID=teamID)
    if file_type != 'dir' and file_type != 'doc' and file_type != 'uml':
        return JsonResponse({'errno': 3100, 'msg': "文件类型未定义"})
    if file_name == ' ':
        return JsonResponse({'errno': 3099, 'msg': "文件名称不得为空"})

# @csrf_exempt
# def create_file(request):
#     if request.method == 'POST':
#         if login_check(request):
#             try:
#                 file_name = request.POST.get('file_name')
#                 user = User.objects.get(userID=request.session['userID'])
#                 isDir = request.POST.get('isDir')
#                 file_type = request.POST.get('file_type')
#                 father_id = request.POST.get('father_id')  # 返回当前文件夹的父节点编号，若当前在根目录下，则返回0
#             except ValueError:
#                 return JsonResponse({'errno': 2001, 'msg': "文件名不得为空"})
#             except Exception as e:
#                 return JsonResponse({'errno': 2000, 'msg': repr(e)})
#             file = File.objects.filter(file_name=file_name, isDelete=False, user=user)
#             if file.count():
#                 return JsonResponse({'errno': 2002, 'msg': "文件名重复"})
#             # else:
#             username = user.username
# 
#             new_file = File(fatherID=father_id,
#                             isDir=file_type,
#                             file_name=file_name,
#                             user=user,
#                             # TeamID=team,
#                             isDelete=False)
#             # How to acquire the directory the file belong to?
#             if 'type' in request.POST:
#                 type = request.POST.get('type')
#                 try:
#                     mode = FileModel.objects.get(m_name=type)
#                 except ObjectDoesNotExist:
#                     return JsonResponse({'errno': 2035, 'msg': "目标模板不存在"})
#                 new_file.content = mode.m_content
# 
#             new_file.save()
#             result = {'errno': 0,
#                       "fileID": new_file.fileID,
#                       'file_name': new_file.file_name,
#                       'create_time': new_file.create_time,
#                       'last_modify_time': new_file.last_modify_time,
#                       'commentFul': new_file.commentFul,
#                       'isDir': new_file.isDir,
#                       'author': new_file.user.username,
#                       'content': new_file.content,
#                       'msg': "新建成功",
#                       "is_fav": new_file.is_fav}
#             return JsonResponse(result)
# 
#         else:
#             return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
#     else:
#         return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})
