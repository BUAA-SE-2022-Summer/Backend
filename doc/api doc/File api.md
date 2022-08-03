### File api

#### Create_file(创建文件)

- 请求方式:POST

- 路由：/api/file/create_file

- 前端request格式

  ```json
  {
  'teamID':xxx,		//	所属团队的ID
  'projectID':xxx,//	所属项目的ID
  'file_name':xxx,	//文件名
  'file_type':xxx,	//文件类型   uml图类型为'uml'，文件夹为'dir'，普通文档类型为'doc'
  'fatherID':xxx		//父文件夹ID		若文件在项目的根目录下，则返回项目的root_file ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0,
  'msg': "新建成功",
  'fileID':xxx, //文件ID
  'file_name':xxx, //文件名
  'create_time': xxx,//创建的时间
  'last_modify_time': xxx,//最后一次修改的时间
  'author': xxx, //创建者姓名
  'file_type': 'uml'/'doc'/'dir',
  'content': xxxx,		//新建文件时，这一项内容为空
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3098, 'msg': '已存在名为' + file_name + '的'+'文档'/'UML类图'/'文件夹'}
    {'errno': 3097, 'msg': "父文件夹不存在"}
    {'errno': 3096, 'msg': "父文件夹错误"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### Edit_file(编辑文件)

- 请求方式:POST

- 路由：/api/file/edit_file

- 前端request格式

  ```json
  {
  'fileID':xxxx,		//文件ID
  'content':xxxxx,	//文件内容
  }
  ```

- 后端response格式

  ```json
  {'errno': 0,
  'msg': "保存成功",
  'fileID':xxx, //文件ID
  'file_name':xxx, //文件名
  'create_time': xxx,//创建的时间
  'last_modify_time': xxx,//最后一次修改的时间
  'editor': xxx, //编辑者姓名
  'file_type': 'uml'/'doc'/'dir',
  'content': xxxx,		//新建文件时，这一项内容为空
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法编辑"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3093, 'msg': "文件已被删除"}
    {'errno': 3092, 'msg': "无法编辑文件夹"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### Read_file(查看文件)

- 请求方式:POST

- 路由：/api/file/read_file

- 前端request格式

  ```json
  {
  'fileID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0,
  'msg': "打开成功",
  'fileID':xxx, //文件ID
  'file_name':xxx, //文件名
  'create_time': xxx,//创建的时间
  'last_modify_time': xxx,//最后一次修改的时间
  'file_type': 'uml'/'doc'/'dir',
  'content': xxxx,		//新建文件时，这一项内容为空
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法查看"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3093, 'msg': "文件已被删除"}
    {'errno': 3092, 'msg': "无法查看文件夹内容"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```





#### delete_file(删除文件（夹）)

> 支持对文件夹的递归删除

- 请求方式:POST

- 路由：/api/file/delete_file

- 前端request格式

  ```json
  {
  'fileID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 'msg': "删除成功"}
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法删除"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3091, 'msg': "无法获取文件信息"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### restore_file(恢复文件（夹）)

> 恢复被删除的文件或文件夹，
>
> 被恢复后，文件将出现在项目的根目录下

- 请求方式:POST

- 路由：/api/file/restore_file

- 前端request格式

  ```json
  {
  'fileID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 'msg': "恢复成功"}
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法恢复"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3091, 'msg': "无法获取文件信息"}
    {'errno': 3090, 'msg': "文件不在回收站中"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### project_root_filelist（获取项目的文件列表）

- 请求方式:POST

- 路由：/api/file/project_root_filelist

- 前端request格式

  ```json
  {
  'projectID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 
   'msg': "成功打开项目", 
   'filelist': [
     {
     'fileID': xxx,
     'file_name': xxx,
     'create_time': xxx,
     'last_modify_time': xxx,
     'file_type': xxx
   		},
     {
     'fileID': xxx,
     'file_name': xxx,
     'create_time': xxx,
     'last_modify_time': xxx,
     'file_type': xxx
   		},
     ……
   ]
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法查看"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3089, 'msg': "无法获取项目信息"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### get_dir_list（获取项目中的某一文件夹列表）

- 请求方式:POST

- 路由：/api/file/get_dir_list

- 前端request格式

  ```json
  {
   'dirID':xxx,//文件夹的ID
  'projectID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 
   'msg': "成功打开文件夹", 
   'dirlist': [
     {
     'fileID': xxx,
     'file_name': xxx,
     'create_time': xxx,
     'last_modify_time': xxx,
     'file_type': xxx
   		},
     {
     'fileID': xxx,
     'file_name': xxx,
     'create_time': xxx,
     'last_modify_time': xxx,
     'file_type': xxx
   		},
     ……
   ]
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法查看"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3089, 'msg': "无法获取项目信息"}
    {'errno': 3088, 'msg': "无法获取目录信息"}
    {'errno': 3087, 'msg': "无法展开非目录文件"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### delete_filelist（项目回收站的文件列表）

- 请求方式:POST

- 路由：/api/file/delete_filelist

- 前端request格式

  ```json
  {
  'projectID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 
   'msg': "成功打开回收站", 
   'dirlist': [
     {
     'fileID': xxx,
     'file_name': xxx,
     'delete_time': xxx,
     'file_type': xxx
   		},
     {
     'fileID': xxx,
     'file_name': xxx,
     'delete_time': xxx,
     'file_type': xxx
   		},
     ……
   ]
  }
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3099, 'msg': "文件名称不得为空"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法查看"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3089, 'msg': "无法获取项目信息"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



