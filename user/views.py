from random import Random
import datetime
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from myUtils.utils import SHA256, check_pwd, validate_phone, validate_email, update_img_file
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def login_check(request):
    return 'userID' in request.session


login_dic = {}


@csrf_exempt
def login(request):
    if request.method == 'POST':
        encoder = SHA256()
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
        if user.password == encoder.hash(password):
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
        encoder = SHA256()
        hash_password = encoder.hash(password)
        new_user = User(username=username, password=hash_password, real_name=real_name, email=email, phone=phone,
                        profile=profile)
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
        data_info = {'username': user.username, 'password': user.password, 'real_name': user.real_name,
                     'email': user.email,
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
        encoder = SHA256()
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
        user.password = encoder.hash(password)
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


@csrf_exempt
def send_code(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '用户名不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        if email == '':
            return JsonResponse({'errno': 3, 'msg': '邮箱不能为空'})
        if not username_exist(username):
            return JsonResponse({'errno': 4, 'msg': '用户尚未注册'})
        if not validate_email(email):
            return JsonResponse({'errno': 5, 'msg': '邮箱格式错误'})
        user = User.objects.get(username=username)
        if user.email != email:
            return JsonResponse({'errno': 6, 'msg': '邮箱与注册邮箱不匹配'})
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
        code = random_str()
        request.session["code"] = code
        request.session["password"] = password
        request.session["username"] = username
        request.session["email"] = email
        htmly = get_template('test.html')
        subject, from_email, to = '重置密码', 'mobook@horik.cn', email
        html_content = htmly.render({'code': code, 'time': datetime.datetime.now().strftime('%Y-%m-%d')})
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to, ])
        msg.content_subtype = 'html'
        msg.attach_alternative('', "text/html")
        msg.send()
        # email_title = "找回密码"
        # email_body = "验证码为：{0}".format(code)
        # send_status = send_mail(email_title, email_body, "mobook@horik.cn", [email, ])
        return JsonResponse({'errno': 0, 'msg': "验证码已发送，请查收邮件"})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})


@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if username == '':
            return JsonResponse({'errno': 1, 'msg': '用户名不能为空'})
        if password == '':
            return JsonResponse({'errno': 2, 'msg': '密码不能为空'})
        if email == '':
            return JsonResponse({'errno': 3, 'msg': '邮箱不能为空'})
        if not username_exist(username):
            return JsonResponse({'errno': 4, 'msg': '用户尚未注册'})
        if not validate_email(email):
            return JsonResponse({'errno': 5, 'msg': '邮箱格式错误'})
        user = User.objects.get(username=username)
        if user.email != email:
            return JsonResponse({'errno': 6, 'msg': '邮箱与注册邮箱不匹配'})
        if code == '':
            return JsonResponse({'errno': 7, 'msg': '验证码不能为空'})
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
        if username == request.session["username"] and email == request.session["email"]:
            if password == request.session["password"]:
                if code == request.session["code"]:
                    encoder = SHA256()
                    user.password = encoder.hash(password)
                    user.save()
                    del request.session["code"]
                    del request.session["username"]
                    del request.session["email"]
                    if num == 3:
                        return JsonResponse({'errno': 0, 'msg': '更新密码成功', 'level': 'above middle'})
                    return JsonResponse({'errno': 200, 'msg': "更新密码成功", 'level': 'strong'})
                else:
                    return JsonResponse({'errno': 9, 'msg': '验证码错误'})
            else:
                return JsonResponse({'errno': 16, 'msg': '两次密码不一致'})
        else:
            return JsonResponse({'errno': 8, 'msg': '用户信息错误'})
    else:
        return JsonResponse({'errno': 10, 'msg': "请求方式错误"})
