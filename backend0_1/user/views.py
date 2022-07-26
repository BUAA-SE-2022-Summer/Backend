from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '':
            return JsonResponse({'error': 1, 'msg': '用户名不能为空'})
        if password == '':
            return JsonResponse({'error': 2, 'msg': '密码不能为空'})
        user = User.objects.get(username=username)
        if user.password == password:
            request.session['username'] = username
            return JsonResponse({'errno': 0, 'msg': "登录成功"})
        else:
            return JsonResponse({'errno': 3, 'msg': "密码错误"})
    else:
        return JsonResponse({'errno': 5, 'msg': "请求方式错误"})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password_1 = request.POST.get('password_1', '')
        password_2 = request.POST.get('password_2', '')
        if username == '':
            return JsonResponse({'error': 1, 'msg': '用户名不能为空'})
        if password_1 == '':
            return JsonResponse({'error': 2, 'msg': '密码不能为空'})
        if password_2 == '':
            return JsonResponse({'error': 3, 'msg': '确认密码不能为空'})
        if password_1 != password_2:
            return JsonResponse({'errno': 4, 'msg': "两次输入的密码不同"})
        new_author = User(username=username, password=password_1)
        new_author.save()
        return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 5, 'msg': "请求方式错误"})


@csrf_exempt
def find_all(request):
    if request.method == 'GET':
        users = User.objects.all()
        return JsonResponse({'errno': 0, 'msg': "查询成功", 'data': users})
    else:
        return JsonResponse({'errno': 5, 'msg': "请求方式错误"})
