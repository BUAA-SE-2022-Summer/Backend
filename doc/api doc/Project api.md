# Project api

#### create_project(创建项目)

- 路由：/api/project/create_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'project_name':xxx,
  	'project_desc':xxx(可空),
      'teamID':xxx,
      
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0, 
      'msg': '创建项目成功',
      'projectID': xxx
  }
  ```

- 错误提示

  - 项目名称为空

    ```json
    {'errno': 1, 'msg': '项目名称不能为空'}
    //名称重复
    {'errno': 2, 'msg': '项目名称已存在'}
    ```

  - 请求方式错误
  
    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录
  
    ```json
    {'errno': 1002, 'msg': "未登录不能创建项目"}
    ```


#### delete_project(删除项目)（伪删除）

- 路由：/api/project/delete_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'projectID':xxx,
      'teamID':xxx,
      
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '删除项目成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限删除该项目'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能删除项目"}
    ```

#### star_project(星标项目)

- 路由：/api/project/star_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'projectID':xxx,
      'teamID':xxx,
      
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '收藏项目成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限收藏该项目'}
    ```

  - 该项目已被收藏

    ```json
    {'errno': 2, 'msg': '该项目已经被收藏'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能收藏项目"}
    ```

#### unstar_project(取消星标项目)

- 路由：/api/project/unstar_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'projectID':xxx,
      'teamID':xxx,
      
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '取消收藏项目成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限取消收藏该项目'}
    ```

  - 该项目未被收藏

    ```json
    {'errno': 2, 'msg': '该项目未被收藏'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能取消收藏项目"}
    ```

#### rename_project(重命名项目)

- 路由：/api/project/rename_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'projectID':xxx,
      'teamID':xxx,
      'project_name'
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '修改项目名称成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限修改该项目名称'}
    ```

  - 项目名称为空

    ```json
    {'errno': 2, 'msg': '项目名称不能为空'}
    //名称重复
    {'errno': 3, 'msg': '项目名称已存在'}
    ```

  - 请求方式错误
  
    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录
  
    ```json
    {'errno': 1002, 'msg': "未登录不能修改项目名称"}
    ```

#### get_project_list(查看该团队所有项目)

- 路由：/api/project/get_project_list

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list}
  project_list = [
      {
                  'projectID': project.projectID,
                  'projectName': project.projectName,
                  'projectDesc': project.projectDesc,
                  'projectImg': project.projectImg,
                  'projectUser': project.projectUser,
                  'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
          		'last_modify_time': project.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
                  'is_star': project.is_star,
      }……
  ]
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### get_star_project_list(查看该团队所有星标项目)

- 路由：/api/project/get_star_project_list

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list}
  project_list = [
      {
                  'projectID': project.projectID,
                  'projectName': project.projectName,
                  'projectDesc': project.projectDesc,
                  'projectImg': project.projectImg,
                  'projectUser': project.projectUser,
                  'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
          		'last_modify_time': project.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
                  'is_star': project.is_star,
      }……
  ]
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### get_create_project_list(查看用户创建项目)

- 路由：/api/project/get_create_project_list

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list}
  project_list = [
      {
                  'projectID': project.projectID,
                  'projectName': project.projectName,
                  'projectDesc': project.projectDesc,
                  'projectImg': project.projectImg,
                  'projectUser': project.projectUser,
                  'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
          		'last_modify_time': project.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
                  'is_star': project.is_star,
      }……
  ]
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### get_delete_project_list(查看回收站项目)

- 路由：/api/project/get_delete_project_list

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '获取项目列表成功', 'project_list': project_list}
  project_list = [
      {
                  'projectID': project.projectID,
                  'projectName': project.projectName,
                  'projectDesc': project.projectDesc,
                  'projectImg': project.projectImg,
                  'projectUser': project.projectUser,
                  'projectTime': project.projectTime.strftime('%Y-%m-%d %H:%M:%S'),
          		'last_modify_time': project.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
                  'is_star': project.is_star,
      }……
  ]
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### delete_project_recycle_bin(回收站彻底删除项目)

- 路由：/api/project/delete_project_recycle_bin

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  	'projectID':xxx
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '删除项目成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 项目不存在

    ```json
    {'errno': 2, 'msg': '该项目不存在'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### cancel_delete_project(回收站撤销删除项目)

- 路由：/api/project/cancel_delete_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  	'projectID':xxx
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '恢复项目成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 项目不存在

    ```json
    {'errno': 2, 'msg': '该项目不存在'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### copy_project(复制项目)

- 路由：/api/project/copy_project

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	'projectID':xxx,
      'projectName':xxx,
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0,
      'msg': '复制项目成功',
      'projectID': xxx,
      'projectName': xxx,
      'projectUser': xxx,
      'project_root_fileID': xxx
  }
  ```

- 错误提示

  - 项目ID获取失败

    ```json
    {'errno': 1, 'msg': "信息获取失败"}
    ```

  - 项目不存在

    ```json
    {'errno': 2, 'msg': "无法获取项目信息"}
    ```

  - 没有权限

    ```json
    {'errno': 3, 'msg': "您不是该团队的成员，无法查看"}
    ```

  - 项目已存在

    ```json
    {'errno': 4, 'msg': "该项目已存在"}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```
  
  - 用户未登录
  
    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

#### empty_recycle_bin(清空回收站)

- 路由：/api/project/empty_recycle_bin

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  	
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '清空回收站成功'}
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限获取该项目列表'}
    ```

  - 回收站为空

    ```json
    {'errno': 2, 'msg': '回收站为空'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取项目列表"}
    ```

