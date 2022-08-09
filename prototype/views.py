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
from prototype.models import PageUse
from django.shortcuts import render
from myUtils.utils import login_check
from itsdangerous import URLSafeTimedSerializer, BadData
from backend.settings import SECRET_KEY


def add_page_use(page, user):
    pageUse = PageUse(page=page, user=user)
    pageUse.save()


def delete_page_use(page, user):
    pageUse = PageUse.objects.filter(page=page, user=user)
    if len(pageUse) == 0:
        return
    pageUse.delete()


def get_page_use_list(page):
    user_list = []
    page_use_list = PageUse.objects.filter(page=page)
    for i in page_use_list:
        user_list.append({'userID': i.user.userID, 'userName': i.user.userName, 'img': i.user.img})
    return user_list


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
            father = File.objects.get(fileID=fatherID, file_type='dir', isDelete=False, team=team, project_id=projectID)
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
        project = Project.objects.get(projectID=projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
        add_page_use(new_page, user)
        user_list = get_page_use_list(new_page)
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
                             'pageCanvasStyle': new_page.pageCanvasStyle,
                             'user_list': user_list,
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
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
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
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
        add_page_use(first_page, user)
        user_list = get_page_use_list(first_page)
        return JsonResponse({'errno': 0,
                             'msg': '打开成功',
                             'namelist': namelist,
                             'first_component': first_page.pageComponentData,
                             'first_canvasStyle': first_page.pageCanvasStyle,
                             'user_list': user_list,
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def delete_prototype(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能删除原型图"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限删除原型图'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pages = Page.objects.filter(prototype=prototype)
        for page in pages:
            user_list = get_page_use_list(page)
            if len(user_list) > 1:
                return JsonResponse({'errno': 2, 'msg': '原型图被使用，不能删除'})
            if len(user_list) == 1 and user_list[0]['userID'] != userID:
                return JsonResponse({'errno': 3, 'msg': '原型图被其他用户使用，不能删除'})
        for page in pages:
            page.delete()
        prototype.delete()
        return JsonResponse({'errno': 0, 'msg': '删除成功'})
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
        old_pageID = request.POST.get('old_pageID', '')
        old_page = Page.objects.get(pageID=old_pageID, prototype=prototype)
        pageID = request.POST.get('pageID', '')
        page = Page.objects.get(pageID=pageID, prototype=prototype)
        componentData = page.pageComponentData
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
        add_page_use(page, user)
        delete_page_use(old_page, user)
        user_list = get_page_use_list(page)
        return JsonResponse({'errno': 0,
                             'msg': '更改成功',
                             'componentData': componentData,
                             'canvasStyle': page.pageCanvasStyle,
                             'user_list': user_list,
                             })
    return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def change_page_name(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能更改页面名称"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限更改页面名称'})
        prototypeID = request.POST.get('prototypeID', '')
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageID = request.POST.get('pageID', '')
        page = Page.objects.get(pageID=pageID, prototype=prototype)
        pageName = request.POST.get('pageName', '')
        if pageName == '':
            return JsonResponse({'errno': 2, 'msg': '页面名称不能为空'})
        page.pageName = pageName
        page.save()
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
        return JsonResponse({'errno': 0,
                             'msg': '更改成功',
                             'pageID': page.pageID,
                             'pageName': pageName
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
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
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
        page_user = PageUse.objects.filter(page=page)
        if len(page_user) > 1:
            return JsonResponse({'errno': 4, 'msg': '页面正在被使用'})
        if len(page_user) == 1 and page_user[0].user != user:
            return JsonResponse({'errno': 4, 'msg': '页面正在被使用'})
        delete_page_use(page, user)
        page.delete()
        pages = Page.objects.filter(prototype=prototype)
        namelist = []
        for page in pages:
            namelist.append({'pageID': page.pageID, 'pageName': page.pageName})
        first_page = Page.objects.get(prototype=prototype, is_first=True)
        project = Project.objects.get(projectID=prototype.projectID)
        project.is_edit = (project.is_edit + 1) % 2
        project.save()
        user_list = get_page_use_list(first_page)
        return JsonResponse({'errno': 0,
                             'msg': '删除成功',
                             'namelist': namelist,
                             'first_component': first_page.pageComponentData,
                             'first_canvasStyle': first_page.pageCanvasStyle,
                             'user_list': user_list
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


def generate_sharing_code(prototypeID):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    data = {'proID': prototypeID}
    token = serializer.dumps(data).encode().decode()
    return token


@csrf_exempt
def share_prototype(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})
    if not login_check(request):
        return JsonResponse({'errno': 1002, 'msg': "请先登录"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        prototypeID = request.POST.get('prototypeID')
    except ValueError:
        return JsonResponse({'errno': 4, 'msg': '信息获取失败'})

    # try:
    prototype = Prototype.objects.get(prototypeID=prototypeID)
    team = prototype.team
    t_u_check = Team_User.objects.filter(team=team, user=user)
    if len(t_u_check) == 0:
        return JsonResponse({'errno': 1, 'msg': '您不具有分享权限'})
    # except prototype.ObjectDoesNotExist:
    #     return JsonResponse({'errno': 5, 'msg': '原型图信息获取错误'})
    # except prototype.MultipleObjectsReturned:
    #     return JsonResponse({'errno': 5, 'msg': '原型图信息获取错误'})
    prototype.is_sharing = True
    prototype.save()
    token = generate_sharing_code(prototypeID)
    return JsonResponse({'errno': 0, 'msg': '成功获取加密串', 'code': token})


def decode_sharing_code(code):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    data = serializer.loads(code)
    proID = data.get('proID')
    return proID


@csrf_exempt
def enter_sharing_link(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})
    if not login_check(request):
        return JsonResponse({'errno': 1002, 'msg': "请先登录"})
    # userID = request.session['userID']
    # user = User.objects.get(userID=userID)
    try:
        code = request.POST.get('code')
    except ValueError:
        return JsonResponse({'errno': 4, 'msg': '信息获取失败'})
    proID = decode_sharing_code(code)
    prototype = Prototype.objects.get(prototypeID=proID)
    if not prototype.is_sharing:
        return JsonResponse({'errno': 5, 'msg': '原型图预览未开启'})
    pages = Page.objects.filter(prototype=prototype)
    namelist = []
    for page in pages:
        namelist.append({'pageID': page.pageID, 'pageName': page.pageName})
    first_page = Page.objects.get(prototype=prototype, is_first=True)
    return JsonResponse({'errno': 0,
                         'msg': '正在进入预览界面',
                         'namelist': namelist,
                         'first_component': first_page.pageComponentData,
                         'first_canvasStyle': first_page.pageCanvasStyle,
                         })


@csrf_exempt
def close_sharing(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})
    if not login_check(request):
        return JsonResponse({'errno': 1002, 'msg': "请先登录"})
    userID = request.session['userID']
    user = User.objects.get(userID=userID)
    try:
        prototypeID = request.POST.get('prototypeID')
    except ValueError:
        return JsonResponse({'errno': 4, 'msg': '信息获取失败'})
    prototype = Prototype.objects.get(prototypeID=prototypeID)
    team = prototype.team
    t_u_check = Team_User.objects.filter(team=team, user=user)
    if len(t_u_check) == 0:
        return JsonResponse({'errno': 1, 'msg': '您不具有分享权限'})
    if not prototype.is_sharing:
        return JsonResponse({'errno': 6, 'msg': '预览功能已关闭'})
    prototype.is_sharing = False
    prototype.save()
    return JsonResponse({'errno': 0, 'msg': '关闭成功'})
