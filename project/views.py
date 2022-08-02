# from django.core.exceptions import ObjectDoesNotExist
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from project.models import Project
# from user.models import User
# from django.shortcuts import render
#
#
# # Create your views here.
# @csrf_exempt
# def create_project(request):
#     from myUtils.utils import login_check
#     if request.method == 'POST':
#         if not login_check(request):
#             return JsonResponse({'errno': 1002, 'msg': "未登录不能创建项目"})
#         userID = request.session['userID']
#         user = User.objects.get(userID=userID)
#         project_name = request.POST.get('project_name', '')
#         project_desc = request.POST.get('project_desc', '')
#         if project_name == '':
#             return JsonResponse({'errno': 1, 'msg': '项目名称不能为空'})
#         if project_desc == '':
#             return JsonResponse({'errno': 2, 'msg': '项目描述不能为空'})
#         if project_img == '':
#             return JsonResponse({'errno': 3, 'msg': '项目图片不能为空'})
#         if project_user == '':
#             return JsonResponse({'errno': 4, 'msg': '项目创建者不能为空'})
#         if project_team == '':
#             return JsonResponse({'errno': 5, 'msg': '项目所属团队不能为空'})
#         try:
#             project = Project.objects.get(projectName=project_name)
#         except ObjectDoesNotExist:
#             project = Project(projectName=project_name, projectDesc=project_desc, projectImg=project_img, projectUser=project_user, projectTeam=project_team)
#             project.save()
#             return JsonResponse({'errno': 0, 'msg': '创建项目成功'})
#         else:
#             return JsonResponse({'errno': 6, 'msg': '项目名称已存在'})