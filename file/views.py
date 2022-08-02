from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def create_file(request):
    if request.method == 'POST':
        if login_check(request):
            try:
                file_name = request.POST.get('file_name')
                user = User.objects.get(userID=request.session['userID'])
                comment = request.POST.get('commentFul')
                file_type = request.POST.get('isDir')
                father_id = request.POST.get('father_id')  # 返回当前文件夹的父节点编号，若当前在根目录下，则返回0
            except ValueError:
                return JsonResponse({'errno': 2001, 'msg': "文件名不得为空"})
            except Exception as e:
                return JsonResponse({'errno': 2000, 'msg': repr(e)})
            file = File.objects.filter(file_name=file_name, isDelete=False, user=user)
            if file.count():
                return JsonResponse({'errno': 2002, 'msg': "文件名重复"})
            # else:
            username = user.username

            new_file = File(fatherID=father_id,
                            isDir=file_type,
                            file_name=file_name,
                            username=username,
                            user=user,
                            commentFul=comment,
                            # TeamID=team,
                            isDelete=False)
            # How to acquire the directory the file belong to?
            if 'type' in request.POST:
                type = request.POST.get('type')
                try:
                    mode = FileModel.objects.get(m_name=type)
                except ObjectDoesNotExist:
                    return JsonResponse({'errno': 2035, 'msg': "目标模板不存在"})
                new_file.content = mode.m_content

            new_file.save()
            result = {'errno': 0,
                      "fileID": new_file.fileID,
                      'file_name': new_file.file_name,
                      'create_time': new_file.create_time,
                      'last_modify_time': new_file.last_modify_time,
                      'commentFul': new_file.commentFul,
                      'isDir': new_file.isDir,
                      'author': new_file.user.username,
                      'content': new_file.content,
                      'msg': "新建成功",
                      "is_fav": new_file.is_fav}
            return JsonResponse(result)

        else:
            return JsonResponse({'errno': 2009, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 2010, 'msg': "请求方式错误"})

