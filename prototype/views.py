from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project.models import Project
from user.models import User
from team.models import Team
from team.models import Team_User
from file.models import File
from prototype.models import Prototype
from prototype.models import Page
from django.shortcuts import render
from myUtils.utils import login_check


# Create your views here.
@csrf_exempt
def create_prototype(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能创建原型图"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        try:
            teamID = request.POST.get('teamID')
            projectID = request.POST.get('projectID')
            fatherID = request.POST.get('fatherID')
            prototypeName = request.POST.get('prototypeName')
        except ValueError:
            return JsonResponse({'errno': 2, 'msg': "信息获取失败"})
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        project = Project.objects.get(projectID=projectID)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限创建原型图'})
        if prototypeName == '':
            return JsonResponse({'errno': 3, 'msg': '原型名称不能为空'})
        try:
# <<<<<<< HEAD
            father = File.objects.get(fileID=fatherID, file_type='文件夹', isDelete=False, team=team, project_id=projectID)
# =======
#             father = File.objects.get(fileID=fatherID, file_type='文件夹', isDelete=False, team=team, project=project)
# >>>>>>> 448da8307c3fb01be5231c68049781e58812f06c
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 3097, 'msg': "父文件夹不存在"})
        except MultipleObjectsReturned:
            return JsonResponse({'errno': 3096, 'msg': "父文件夹错误"})
        new_prototype = Prototype(prototypeName=prototypeName, prototypeUser=userID, fatherID=fatherID,
                                  team=team, projectID=projectID)
        new_page = Page(pageName='首页', pageUser=userID, is_first=True, prototype=new_prototype)
        new_prototype.save()
        new_page.save()
        return JsonResponse({'errno': 0,
                             'msg': '创建成功',
                             'prototypeID': new_prototype.prototypeID,
                             'prototypeName': new_prototype.prototypeName,
                             'create_time': new_prototype.create_time,
                             'last_modify_time': new_prototype.last_modify_time,
                             'author': user.username,
                             'file_type': new_prototype.file_type,
                             'pageID': new_page.pageID,
                             'pageName': new_page.pageName,
                             'pageComponentData': new_page.pageComponentData,
                             'pageCanvasStyle': new_page.pageCanvasStyle
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def create_page(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能创建页面"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限创建页面'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageName = request.POST.get('pageName', '')
        if pageName == '':
            return JsonResponse({'errno': 2, 'msg': '页面名称不能为空'})
        new_page = Page(pageName=pageName, pageUser=userID, prototype=prototype)
        new_page.save()
        return JsonResponse({'errno': 0,
                             'msg': '创建成功',
                             'pageID': new_page.pageID,
                             'pageName': pageName
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def open_prototype(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能打开原型图"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限打开原型图'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pages = Page.objects.filter(prototype=prototype)
        namelist = []
        for page in pages:
            namelist.append({'pageID': page.pageID, 'pageName': page.pageName})
        first_page = Page.objects.get(prototype=prototype, is_first=True)
        return JsonResponse({'errno': 0,
                             'msg': '打开成功',
                             'namelist': namelist,
                             'first_component': first_page.pageComponentData,
                             'first_canvasStyle': first_page.pageCanvasStyle,
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def change_page(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能更改页面"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限更改页面'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageID = request.POST.get('pageID', '')
        page = Page.objects.get(pageID=pageID, prototype=prototype)
        componentData = page.pageComponentData
        return JsonResponse({'errno': 0,
                             'msg': '更改成功',
                             'componentData': componentData,
                             'canvasStyle': page.pageCanvasStyle,
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def update_page(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能更改页面"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限更改页面'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageID = request.POST.get('pageID', '')
        page = Page.objects.get(pageID=pageID, prototype=prototype)
        pageComponentData = request.POST.get('pageComponentData', '')
        pageCanvasStyle = request.POST.get('pageCanvasStyle', '')
        page.pageComponentData = pageComponentData
        page.pageCanvasStyle = pageCanvasStyle
        page.save()
        return JsonResponse({'errno': 0,
                             'msg': '更改成功',
                             'componentData': pageComponentData,
                             'canvasStyle': pageCanvasStyle,
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def delete_page(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能删除页面"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限删除页面'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageID = request.POST.get('pageID', '')
        try:
            page = Page.objects.get(pageID=pageID, prototype=prototype)
        except Page.DoesNotExist:
            return JsonResponse({'errno': 2, 'msg': '页面不存在'})
        if page.is_first:
            return JsonResponse({'errno': 3, 'msg': '不能删除首页'})
        page.delete()
        pages = Page.objects.filter(prototype=prototype)
        namelist = []
        for page in pages:
            namelist.append({'pageID': page.pageID, 'pageName': page.pageName})
        first_page = Page.objects.get(prototype=prototype, is_first=True)
        return JsonResponse({'errno': 0,
                             'msg': '删除成功',
                             'namelist': namelist,
                             'first_component': first_page.pageComponentData,
                             'first_canvasStyle': first_page.pageCanvasStyle
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


def get_prototype_list(fatherID, projectID, allow_del, user, is_personal):
    res = []
    if is_personal:
        prototype_list = Prototype.objects.filter(fatherID=fatherID, projectID=projectID, prototypeUser=user)
    else:
        prototype_list = Prototype.objects.filter(fatherID=fatherID, projectID=projectID)
    for i in prototype_list:
        if not (i.is_delete and not allow_del):
            # author = User.objects.get(userID=i.prototypeUser)
            res.append({
                'fileID': i.prototypeID,
                'file_name': i.prototypeName,
                'create_time': i.create_time,
                'last_modify_time': i.last_modify_time,
                'file_type': 'pro'
            })
    return res
