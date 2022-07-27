# 检查是否已登录
def login_check(request):
    return 'userID' in request.session
