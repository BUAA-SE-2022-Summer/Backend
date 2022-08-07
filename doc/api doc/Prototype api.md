# Prototype api

#### create_prototype(创建原型图)

- 路由：/api/prototype/create_prototype

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
  	'prototypeName':xxx,
      'fatherID':xxx,
      'projectID':xxx
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '创建成功', 'data': datalist}
  datalist = {
      'errno': 0,
      'msg': '创建成功',
      'prototypeID': xxx,
      'prototypeName': xxx,
      'create_time': xxx,
      'last_modify_time': xxx,
      'author': xxx,
      'file_type': xxx,
      'pageID': xxx,
      'pageName': xxx,
      'pageComponentData': xxx,
      'pageCanvasStyle': xxx
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限创建原型图'}
    ```

  - 名称为空

    ```json
    {'errno': 2, 'msg': '原型名称不能为空'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能创建原型图"}
    ```

#### create_page(创建页面)

- 路由：/api/prototype/create_page

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
  	'pageName':xxx
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0,
      'msg': '创建成功',
      'pageID': new_page.pageID,
      'pageName': pageName
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限创建页面'}
    ```

  - 名称为空

    ```json
    {'errno': 2, 'msg': '页面名称不能为空'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能创建页面"}
    ```

#### open_prototype(打开原型图)

- 路由：/api/prototype/open_prototype

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0,
      'msg': '打开成功',
      'namelist': [
          {
          'pageID': xxx, 
          'pageName': xxx
          }
          ……
      ],
      'first_component': xxx,
      'first_canvasStyle': xxx
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限打开原型图'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能打开原型图"}
    ```

#### change_page(切换页面)

- 路由：/api/prototype/change_page

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
      'pageID':xxx,
      
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0, 
      'msg': '更改成功', 
      'componentData': "[{xxx},……]",
      'canvasStyle': xxx
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限更改页面'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能更改页面"}
    ```

#### change_page_name(切换页面)

- 路由：/api/prototype/change_page_name

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
      'pageID':xxx,
      'pageName':xxx
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0, 
      'msg': '更改成功',
      'pageID': page.pageID,
      'pageName': pageName
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限更改页面名称'}
    ```

  - 页面名称为空

    ```json
    {'errno': 2, 'msg': '页面名称不能为空'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能更改页面名称"}
    ```

#### update_page(更改页面)

- 路由：/api/prototype/update_page

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
      'pageID':xxx,
      'pageComponentData':[{xxx},……],
      'pageCanvasStyle':xxx
  }
  ```

- 后端response:

  ```json
  {
  	'errno': 0,
      'msg': '更改成功',
      'componentData': xxx,
      'canvasStyle': xxx,
  
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限更改页面'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能更改页面"}
    ```

#### delete_page(删除页面)

- 路由：/api/prototype/delete_page

- 请求方式：POST

- 前端request格式：

  ```json
  {
      'teamID':xxx,
      'prototypeID':xxx,
      'pageID':xxx,
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0,
      'msg': '删除成功',
      'namelist': [
          {
          'pageID': xxx, 
          'pageName': xxx
          }
          ……
      ],
      'first_component': xxx,
      'first_canvasStyle': xxx
  }
  ```

- 错误提示

  - 没有权限

    ```json
    {'errno': 1, 'msg': '没有权限删除页面'}
    ```

  - 页面不存在

    ```json
    {'errno': 2, 'msg': '页面不存在'}
    ```

  - 删除首页

    ```json
    {'errno': 3, 'msg': '不能删除首页'}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能删除页面"}
    ```



