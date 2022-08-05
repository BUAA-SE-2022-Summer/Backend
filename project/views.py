from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from project.models import Project
from user.models import User
from team.models import Team
from team.models import Team_User
from django.shortcuts import render
from file.models import File


# Create your views here.
@csrf_exempt
def create_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能创建项目"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        project_name = request.POST.get('project_name', '')
        project_desc = request.POST.get('project_desc', '')
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        if project_name == '':
            return JsonResponse({'errno': 1, 'msg': '项目名称不能为空'})
        new_project = Project(projectName=project_name, projectDesc=project_desc,
                              projectUser=user.userID, team=team)
        new_project.save()

        root_file = File(fatherID=-1, file_type='dir', file_name='root', isDelete=False, team=team,
                         project_id=new_project.projectID)
        root_file.save()
        new_project.root_file_id = root_file.fileID
        new_project.save()
        return JsonResponse({'errno': 0, 'msg': '创建项目成功', 'projectID': new_project.projectID,
                             'project_root_fileID': root_file.fileID})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def delete_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能删除项目"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        projectID = request.POST.get('projectID', '')
        project = Project.objects.get(projectID=projectID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限删除该项目'})
        project.is_delete = True
        project.save()
        return JsonResponse({'errno': 0, 'msg': '删除项目成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def star_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能收藏项目"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        projectID = request.POST.get('projectID', '')
        project = Project.objects.get(projectID=projectID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限收藏该项目'})
        if project.is_star is True:
            return JsonResponse({'errno': 2, 'msg': '该项目已经被收藏'})
        project.is_star = True
        project.save()
        return JsonResponse({'errno': 0, 'msg': '收藏项目成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def unstar_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能取消收藏项目"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        projectID = request.POST.get('projectID', '')
        project = Project.objects.get(projectID=projectID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限取消收藏该项目'})
        if project.is_star is False:
            return JsonResponse({'errno': 2, 'msg': '该项目未被收藏'})
        project.is_star = False
        project.save()
        return JsonResponse({'errno': 0, 'msg': '取消收藏项目成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def rename_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能修改项目名称"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        projectID = request.POST.get('projectID', '')
        project = Project.objects.get(projectID=projectID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限修改该项目名称'})
        new_projectName = request.POST.get('project_name', '')
        if new_projectName == '':
            return JsonResponse({'errno': 2, 'msg': '项目名称不能为空'})
        project.projectName = new_projectName
        project.save()
        return JsonResponse({'errno': 0, 'msg': '修改项目名称成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def get_project_list(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projects = Project.objects.filter(team=team, is_delete=False)
        project_list = []
        for project in projects:
            project_list.append({
                'projectID': project.projectID,
                'projectName': project.projectName,
                'projectDesc': project.projectDesc,
                'projectImg': project.projectImg,
                'projectUser': project.projectUser,
                'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
                'is_star': project.is_star,
                'project_root_fileID': project.root_file_id  # .fileID
            })
        return JsonResponse({'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def get_star_project_list(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projects = Project.objects.filter(team=team, is_delete=False, is_star=True)
        project_list = []
        for project in projects:
            project_list.append({
                'projectID': project.projectID,
                'projectName': project.projectName,
                'projectDesc': project.projectDesc,
                'projectImg': project.projectImg,
                'projectUser': project.projectUser,
                'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
                'is_star': project.is_star,
            })
        return JsonResponse({'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def get_create_project_list(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projects = Project.objects.filter(team=team, is_delete=False, projectUser=user.userID)
        project_list = []
        for project in projects:
            project_list.append({
                'projectID': project.projectID,
                'projectName': project.projectName,
                'projectDesc': project.projectDesc,
                'projectImg': project.projectImg,
                'projectUser': project.projectUser,
                'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
                'is_star': project.is_star,
            })
        return JsonResponse({'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def get_delete_project_list(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projects = Project.objects.filter(team=team, is_delete=True)
        project_list = []
        for project in projects:
            project_list.append({
                'projectID': project.projectID,
                'projectName': project.projectName,
                'projectDesc': project.projectDesc,
                'projectImg': project.projectImg,
                'projectUser': project.projectUser,
                'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
                'is_star': project.is_star,
            })
        return JsonResponse({'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def delete_project_recycle_bin(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projectID = request.POST.get('projectID', '')
        try:
            project = Project.objects.get(projectID=projectID, is_delete=True)
            project.delete()
        except:
            return JsonResponse({'errno': 2, 'msg': '该项目不存在'})
        return JsonResponse({'errno': 0, 'msg': '删除项目成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})


@csrf_exempt
def cancel_delete_project(request):
    from myUtils.utils import login_check
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取项目列表"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        teamID = request.POST.get('teamID', '')
        team = Team.objects.get(teamID=teamID)
        users = Team_User.objects.filter(user=user, team=team)
        if len(users) == 0:
            return JsonResponse({'errno': 1, 'msg': '没有权限获取该项目列表'})
        projectID = request.POST.get('projectID', '')
        try:
            project = Project.objects.get(projectID=projectID, is_delete=True)
            project.is_delete = False
            project.save()
        except:
            return JsonResponse({'errno': 2, 'msg': '该项目不存在'})
        return JsonResponse({'errno': 0, 'msg': '恢复项目成功'})
    else:
        return JsonResponse({'errno': 10, 'msg': '请求方式错误'})
