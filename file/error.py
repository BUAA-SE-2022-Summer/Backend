from django.http import JsonResponse


def method_err():
    return JsonResponse({'errno': 3001, 'msg': "请求方式错误"})


def not_login_err():
    return JsonResponse({'errno': 3002, 'msg': "用户未登录"})


def name_duplicate_err(file_type, file_name):
    dic = {'doc': '文档', 'uml': 'UML类图', 'dir': '文件夹'}
    error_type = dic[file_type]
    # error_type = file_type
    # if file_type == 'doc':
    #     error_type = '文档'
    # elif file_type == 'uml':
    #     error_type = 'UML类图'
    # else:
    #     error_type = '文件夹'
    return JsonResponse({'errno': 3098, 'msg': '已存在名为' + file_name + '的'+error_type})


def base_err_check(request):
    if request.method != 'POST':
        return method_err()
    if not login_check(request):
        return not_login_err()

