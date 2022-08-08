### 文档中心新增 api

#### Create_team_file(创建团队文件)

> 这类文件直属于团队，不属于团队下任何项目；
>
> 此类文件支持嵌套多层文件夹（可套娃）

- 请求方式:POST

- 路由：/api/file/create_team_file

- 前端request格式

  ```json
  {
  'teamID':xxx,		//	所属团队的ID
  'file_name':xxx,	//文件名
  'file_type':xxx,	//文件类型   'doc'为文件，'dir'为文件夹
  'fatherID':xxx		//父文件夹ID		此为团队文件所在的父文件夹id；若该文件直接建在团队文件下，请返回0
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
    {'errno': 3095, 'msg': "您不是该团队的成员，无法创建文件"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```



#### get_file_centre_list(获取文档中心的团队文档列表)

> 这类文件直属于团队，不属于团队下任何项目；
>
> 此类文件支持嵌套多层文件夹

- 请求方式:POST

- 路由：/api/file/get_file_centre_list

- 前端request格式

  ```json
  {
  'teamID':xxx,		//	所属团队的ID
  }
  ```

- 后端response格式

  > 注意：以下内容的套娃含量较高

  ```json
  {
      "errno": 0,
      "msg": "团队文件列表获取成功",
      "items": [
          {
              "id": 45,
              "name": "Crown",
              "is_dir": true,			//是否为文件夹：True表示是文件夹
              "is_pro": true,			//是否为项目： True表示是项目；False表示不是项目，仅仅是团队直属的文件（夹）
              "children": [
                  {
                      "id": 69,
                      "name": "西江月",
                      "is_dir": false,
                      "is_pro": false
                  },
                  {
                      "id": 70,
                      "name": "白蘋香",
                      "is_dir": false,
                      "is_pro": false
                  },
                  {
                      "id": 71,
                      "name": "玉炉三涧雪",
                      "is_dir": false,
                      "is_pro": false
                  }
              ]
          },	
        //此处以上是projectID为45、名为"Crown"的项目下的所有文档（项目内不含文件夹），其中三个文档的fileID分别为69、70、71
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
                      "is_pro": false
                  },
                  {
                      "id": 74,
                      "name": "横塘路",
                      "is_dir": false,
                      "is_pro": false
                  }
              ]
          },		//此处以上是项目ID为46、名为"啊啊啊啊啊"的项目下的文档（项目内不含文件夹），具体含义同上
          {
              "id": 75,
              "name": "青莲池上客",
              "is_dir": false,
              "is_pro": false
          },	//这一字典表示fileID=75的团队文档，这一文档不属于任何项目
          {
              "id": 76,
              "name": "hhhh",
              "is_dir": false,
              "is_pro": false
          },//同上
          {//以下是fileID=77的团队文件夹（区别于项目）；这一文件夹下含有两个fileID分别为79、80的文档、一个fileID=81的文件夹
              "id": 77,
              "name": "江南无所有",
              "is_dir": true,
              "is_pro": false,
              "children": [
                  {
                      "id": 79,
                      "name": "疏影",
                      "is_dir": false,
                      "is_pro": false
                  },
                  {
                      "id": 80,
                      "name": "莳花",
                      "is_dir": false,
                      "is_pro": false
                  },
                  {
                      "id": 81,					//以下为fileID=81的文件夹，内部仍可新建文件夹
                      "name": "柳迷",
                      "is_dir": true,
                      "is_pro": false,
                      "children": [
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
                          }
                      ]
                  }
              ]
          },
          {
              "id": 78,
              "name": "聊赠一枝春",
              "is_dir": true,
              "is_pro": false,
              "children": []
          }
      ]
  }
  ```

  - 异常处理

    ```json
    {'errno': 3095, 'msg': "您不是该团队的成员，无法查看"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3001, 'msg': "请求方式错误"}
    ```

