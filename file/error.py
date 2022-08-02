from django.http import JsonResponse


def method_err():
    return JsonResponse({'errno': 3001, 'msg': "请求方式错误"})


def not_login_err():
    return JsonResponse({'errno': 3002, 'msg': "用户未登录"})




