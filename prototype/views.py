from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project.models import Project
from user.models import User
from team.models import Team
from team.models import Team_User
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
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限创建原型图'})
        prototypeName = request.POST.get('prototypeName', '')
        if prototypeName == '':
            return JsonResponse({'errno': 2, 'msg': '原型名称不能为空'})
        new_prototype = Prototype(prototypeName=prototypeName, prototypeUser=userID)
        new_page = Page(pageName='首页', pageUser=userID, is_first=True, prototype=new_prototype)
        new_prototype.save()
        new_page.save()
        datalist = {'prototypeID': new_prototype.prototypeID, 'prototypeName': new_prototype.prototypeName,
                    'pageID': new_page.pageID, 'pageName': new_page.pageName,
                    'pageComponentData': new_page.pageComponentData}
        return JsonResponse({'errno': 0, 'msg': '创建成功', 'data': datalist})
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
        return JsonResponse({'errno': 0, 'msg': '创建成功', 'pageID': new_page.pageID})
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
        datalist = {'namelist': namelist, 'first_component': first_page.pageComponentData}
        return JsonResponse({'errno': 0, 'msg': '打开成功', 'data': datalist})
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
        # test = []
        # a = {"component": "v-text", "label": "文字", "propValue": "文字", "icon": "el-icon-edit", "animations": [],
        #      "events": {}, "style": {"width": 200, "height": 33, "fontSize": 14}}
        # test.append(a)
        # print(test)
        return JsonResponse({'errno': 0, 'msg': '更改成功', 'componentData': componentData})
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
        page.pageComponentData = pageComponentData
        page.save()
        return JsonResponse({'errno': 0, 'msg': '更改成功', 'componentData': pageComponentData})
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
        datalist = {'namelist': namelist, 'first_component': first_page.pageComponentData}
        return JsonResponse({'errno': 0, 'msg': '删除成功', 'data': datalist})
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})
