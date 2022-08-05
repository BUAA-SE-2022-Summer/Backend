import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import oss2
import configparser
import os
from pathlib import Path
import re
from string import digits, ascii_lowercase, ascii_uppercase

BASE_DIR = Path(__file__).resolve().parent.parent
cf = configparser.ConfigParser()
cf.read(os.path.join(BASE_DIR, 'Config/django.conf'))

# cf.read('./Config/django.conf')

auth = oss2.Auth(cf.get('data', 'USER'), cf.get('data', 'PWD'))
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
bucket = oss2.Bucket(auth, endpoint, 'xuemolan')
base_image_url = 'https://xuemolan.oss-cn-hangzhou.aliyuncs.com/'


def check_pwd(pwd):
    if not isinstance(pwd, str) or len(pwd) < 8:
        return 11
    r = [False] * 4
    for ch in pwd:
        if ch is ' ':
            return 15
        if not r[0] and ch in digits:
            r[0] = True
        elif not r[1] and ch in ascii_lowercase:
            r[1] = True
        elif not r[2] and ch in ascii_uppercase:
            r[2] = True
        elif not r[3] and ch in ',<.>/?!;:[]{}()*&^%$#@~`':
            r[3] = True
    if r.count(True) < 3:
        if r.count(True) == 0:
            return 12
        if r.count(True) == 1:
            return 13
        if r.count(True) == 2:
            return 14
    return r.count(True)


def validate_phone(phone):
    ret = re.match(r"^1[35678]\d{9}$", phone)
    if ret:
        return True
    else:
        return False


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def update_img_file(image, userID):
    # number = uuid.uuid4()
    base_img_name = str(userID) + '.jpg'
    image_name = base_image_url + base_img_name
    res = bucket.put_object(base_img_name, image)
    if res.status == 200:
        return image_name
    else:
        return False


def login_check(request):
    return 'userID' in request.session


login_dic = {}


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '昵称不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        print(username, password)
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'errno': 1001, 'msg': '用户不存在'})
        if user.password == password:
            request.session['userID'] = user.userID
            login_dic[user.username] = request.session
            return JsonResponse({'errno': 0, 'msg': "登录成功"})
        else:
            return JsonResponse({'errno': 3, 'msg': "密码错误"})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


def username_exist(username):
    user_list = User.objects.filter(username=username)
    return len(list(user_list)) != 0


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        real_name = request.POST.get('real_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        profile = request.POST.get('profile', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '昵称不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        if password_confirm == '':
            return JsonResponse({'errno': 3, 'msg': '确认密码不能为空'})
        if email == '':
            return JsonResponse({'errno': 4, 'msg': '邮箱不能为空'})
        if not validate_email(email):
            return JsonResponse({'errno': 5, 'msg': '邮箱格式错误'})
        if phone != '' and not validate_phone(phone):
            return JsonResponse({'errno': 6, 'msg': '手机号格式错误'})
        if username_exist(username):  # 昵称不重复
            return JsonResponse({'errno': 7, 'msg': "昵称已存在"})
        if password != password_confirm:
            return JsonResponse({'errno': 8, 'msg': '两次密码不一致'})
        num = check_pwd(password)
        if num == 11:
            return JsonResponse({'errno': 11, 'msg': '密码长度不能小于8位'})
        if num == 12:
            return JsonResponse({'errno': 12, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'weak'})
        if num == 13:
            return JsonResponse({'errno': 13, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'below middle'})
        if num == 14:
            return JsonResponse({'errno': 14, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'middle'})
        if num == 15:
            return JsonResponse({'errno': 15, 'msg': '密码包含非法字符'})
        new_user = User(username=username, password=password, real_name=real_name, email=email, phone=phone, profile=profile)
        new_user.save()
        if num == 3:
            return JsonResponse({'errno': 0, 'msg': '注册成功', 'level': 'above middle'})
        return JsonResponse({'errno': 200, 'msg': "注册成功", 'level': 'strong'})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


@csrf_exempt
def logout(request):
    if request.method == 'GET':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能登出"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        request.session.flush()
        login_dic.pop(user.username)
        return JsonResponse({'errno': 0, 'msg': "注销成功"})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


@csrf_exempt
def get_user_info(request):
    if request.method == 'GET':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能获取用户信息"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        data_info = {'username': user.username, 'password': user.password, 'real_name': user.real_name, 'email': user.email,
                     'phone': user.phone, 'profile': user.profile, 'img': user.img}
        return JsonResponse({'errno': 0, 'msg': "获取用户信息成功", 'data': data_info})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


@csrf_exempt
def update_user_info(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能修改用户信息"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        real_name = request.POST.get('real_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        profile = request.POST.get('profile', '')
        if username == '':
            return JsonResponse({'errno': 3, 'msg': '昵称不能为空'})
        if password == '':
            return JsonResponse({'errno': 4, 'msg': '密码不能为空'})
        if email != '' and not validate_email(email):
            return JsonResponse({'errno': 1, 'msg': '邮箱格式错误'})
        if phone != '' and not validate_phone(phone):
            return JsonResponse({'errno': 2, 'msg': '手机号格式错误'})
        num = check_pwd(password)
        if num == 11:
            return JsonResponse({'errno': 11, 'msg': '密码长度不能小于8位'})
        if num == 12:
            return JsonResponse({'errno': 12, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'weak'})
        if num == 13:
            return JsonResponse({'errno': 13, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'below middle'})
        if num == 14:
            return JsonResponse({'errno': 14, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'middle'})
        if num == 15:
            return JsonResponse({'errno': 15, 'msg': '密码包含非法字符'})
        user.username = username
        user.password = password
        user.real_name = real_name
        user.email = email
        user.phone = phone
        user.profile = profile
        user.save()
        if num == 3:
            return JsonResponse({'errno': 0, 'msg': '修改用户信息成功', 'level': 'above middle'})
        return JsonResponse({'errno': 200, 'msg': "修改用户信息成功", 'level': 'strong'})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


@csrf_exempt
def update_user_img(request):
    if request.method == 'POST':
        if not login_check(request):
            return JsonResponse({'errno': 1002, 'msg': "未登录不能修改用户头像"})
        userID = request.session['userID']
        user = User.objects.get(userID=userID)
        img = request.FILES.get('img').read()
        img_url = update_img_file(img, user.userID)
        user.img = img_url
        user.save()
        return JsonResponse({'errno': 0, 'msg': "修改用户头像成功", 'url': img_url})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


