### 回收站系列 api

#### delete_file(删除文件（夹）) 

> 支持对文件夹的递归删除
>
> 这一接口对于【项目文档】和【文档中心的文档】皆适用

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

> 用于恢复被删除的文件或文件夹
>
> 这一接口对于【项目文档】和【文档中心的文档】皆适用
>
> 若恢复的是项目中的文档，则文档会回到项目下；
>
> 若恢复的是文档中心的团队文档（不属于任何项目的文档），则无论其原来的父文件夹是什么，被恢复后都会回到文档中心的根目录下

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

#### completely_delete_file(恢复文件（夹）)

> 用于彻底删除 被删除的文件或文件夹（彻底删除后不可恢复）
>
> 这一接口对于【项目文档】和【文档中心的文档】皆适用

- 请求方式:POST

- 路由：/api/file/completely_delete_file

- 前端request格式

  ```json
  {
  'fileID':xxxx,		//文件ID
  }
  ```

- 后端response格式

  ```json
  {'errno': 0, 'msg': "彻底删除成功"}
  ```

  - 异常处理

    ```json
    {'errno': 3100, 'msg': "文件类型非法"}
    {'errno': 3095, 'msg': "您不是该团队的成员，无法恢复"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3091, 'msg': "无法获取文件信息"}
    {'errno': 3086, 'msg': "请现将文档移入回收站"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### delete_filelist_in_project（项目回收站的文件列表）

> 仅可查看某一项目中被删除的文档

- 请求方式:POST

- 路由：/api/file/delete_filelist_in_project

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
   'delete_filelist': [
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

#### delete_filelist_in_centre(获取文档中心的回收站列表)

- 请求方式:POST

- 路由：/api/file/delete_filelist_in_centre

- 前端request格式

  ```json
  {
  'teamID':xxx,		//	所属团队的ID
  }
  ```

- 后端response格式

  ```json
  {
      "errno": 0,
      "msg": "文档中心回收站列表获取成功",
      "items": [
          {	
              "id": 45,
              "name": "Crown",
              "is_dir": true,
              "is_pro": true,
              "children": []
          },					//以上是projectID=45的项目，这一项目中没有被删除的文件
          {
              "id": 46,
              "name": "啊啊啊啊啊",
              "is_dir": true,
              "is_pro": true,
              "children": [
                  {
                      "id": 73,
                      "name": "青玉案",
                      "is_dir": false,
                      "is_pro": true
                  }
              ]
          },				//以上是projectID=46的项目，这一项目中有一个被删除文件
          {
              "id": 82,
              "name": "云绮",
              "is_dir": true,
              "is_pro": false,
              "children": [
                  {
                      "id": 83,
                      "name": "箫怨",
                      "is_dir": false,
                      "is_pro": false
                  }
              ]
          }				//以上是被删除的fileID=82的团队文件夹，文件夹内有一团队文档
      ]
  }
  ```
  
  - 异常处理

    ```json
    {'errno': 3095, 'msg': "您不是该团队的成员，无法进入文档中心回收站"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```

