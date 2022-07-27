from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User

login_dic = {}


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '用户名不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 1001, 'msg': '用户名不存在'})
        if user.password == password:
            # request.session['username'] = username
            request.session['useID'] = user.userID
            login_dic[user.username] = request.session
            return JsonResponse({'errno': 0, 'msg': "登录成功"})
        else:
            return JsonResponse({'errno': 3, 'msg': "密码错误"})
    else:
        return JsonResponse({'errno': 5, 'msg': "请求方式错误"})


def username_exist(username):
    user_list = User.objects.filter(username=username)
    return len(list(user_list)) != 0


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # password_1 = request.POST.get('password_1', '')
        # password_2 = request.POST.get('password_2', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '用户名不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        # if password_1 == '':
        #     return JsonResponse({'error': 2, 'msg': '密码不能为空'})
        # if password_2 == '':
        #     return JsonResponse({'error': 3, 'msg': '确认密码不能为空'})
        # if password_1 != password_2:
        #     return JsonResponse({'errno': 4, 'msg': "两次输入的密码不同"})
        if username_exist(username):  # 用户名不重复
            return JsonResponse({'errno': 3, 'msg': "用户名已存在"})
        new_user = User(username=username, password=password)
        new_user.save()
        return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 4, 'msg': "请求方式错误"})


@csrf_exempt
def find_all(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_list = []
        for i in users:
            user_list.append({"userID": i.userID,
                              "username": i.username})
        return JsonResponse({'errno': 0, 'msg': "查询成功", 'data': user_list})
    else:
        return JsonResponse({'errno': 5, 'msg': "请求方式错误"})
