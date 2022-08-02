## Team 

#### Create_team(创建团队)

- 路由：/api/team/create_team

- POST

- 前端请求格式

  ```json
  {'team_name':xxx}
  ```

- 后端返回格式

  ```json
  {'errno': 0,
   'msg': "新建团队成功",
   'teamID': xxx,
   'create_time': "2022-08-01T13:03:30.396Z",
   'creator':abc}
  ```

- 异常处理

  ```json
  //无法获取团队名称
  {'errno': 2100, 'msg': "请输入团队名称"}
  //团队名称为空
  {'errno': 2099, 'msg': "团队名称不能为空"}
  //团队名称与已有团队重复
  {'errno': 2098, 'msg': "团队名称重复，取个新名字吧～"}
  ```

  

  #### invite_member(邀请成员)

- 路由：/api/team/invite_member

- POST

- 前端请求格式

  ```json
  {'username':xxx,		//被邀请者的昵称
   'teamID':xxx				//团队ID
  }
  ```

- 后端返回格式

  ```json
  {'errno': 0, 'msg': "邀请成功"}
  ```

- 异常处理

  ```json
  {'errno': 2096, 'msg': "信息获取失败"}
  
  //邀请的用户不存在
  {'errno': 2095, 'msg': "您邀请的用户不存在"}
  
  //无法获取团队id
  {'errno': 2094, 'msg': "无法获取团队id"}
  
  //团队不存在
  {'errno': 2093, 'msg': "团队不存在"}
  
  //无法获取团队信息
  {'errno': 2092, 'msg': "无法获取团队信息"}
  
  //操作者不是团队管理员
  {'errno': 2093, 'msg': "您不具备该团队的管理员权限"}
  
  //被邀请者已在团队中
  {'errno': 2091, 'msg': "您邀请的用户已在团队中"}
  ```



#### kick_member(踢除成员)

- 路由：/api/team/kick_member

- POST

- 前端请求格式

  ```json
  {
   'teamID':xxx,			//团队ID
   'username':xxx,		//被踢除成员的昵称
  }
  ```

- 后端返回格式

  ```json
  {'errno': 0, 'msg': "踢除成功"}
  ```

- 异常处理

  ```json
  {'errno': 2094, 'msg': "无法获取团队id"}
  
  //无法获取被踢除者信息
  {'errno': 2096, 'msg': "成员信息获取失败"}
  
  {'errno': 2093, 'msg': "团队不存在"}
  
  {'errno': 2092, 'msg': "无法获取团队信息"}
  
  //操作者不是团队管理员
  {'errno': 2093, 'msg': "您不是团队管理员，无法踢除其他团队成员"}
  
  //被踢除的用户不存在
  {'errno': 2095, 'msg': "您要踢除的用户不存在"}
  
  //用户本就不属于该团队
  {'errno': 2091, 'msg': "无法踢除不在团队中的用户"}
  
  {'errno': 2093, 'msg': "您不能把自己踢除团队哟～"}
  
  ```

  

#### set_manager(添加管理员)

- 路由：/api/team/set_manager

- POST

- 前端请求格式

  ```json
  {'username':xxx,		//新管理员的昵称
   'teamID':xxx				//团队ID
  }
  ```

- 后端返回格式

  ```json
  {'errno': 0, 'msg': "设置成功"}
  ```

- 异常处理

  ```json
  //无法通过username获取该成员信息
  {'errno': 2095, 'msg': "用户不存在"}
  {'errno': 2094, 'msg': "信息获取失败"}
  
  {'errno': 2093, 'msg': "团队不存在"}
  {'errno': 2093, 'msg': "您不具备管理员权限"}
  
  {'errno': 2092, 'msg': "无法获取团队信息"}
  //无法将团队外成员设置为管理员
  {'errno': 2091, 'msg': "用户不在团队中"}
  
  {'errno': 2090, 'msg': "用户已是管理员"}
  ```

  

#### get_team_info(查看团队信息)

- 路由：/api/team/get_team_info

- POST

- 前端请求格式

  ```json
  {
   'teamID':xxx				//团队ID
  }
  ```

- 后端返回格式

  ```json
  {'errno': 0, 
   'msg': "查看成功", 
   'user_list': [
   		{'username': xxx,	//	成员昵称
       'real_name': xxx,//	成员真实名称
       'email': xxx@xxx,//	成员邮箱
       'is_supervisor': True/False		//成员是否为管理员
      },
   		{'username': xxx,	//	成员昵称
       'real_name': xxx,//	成员真实名称
       'email': xxx@xxx,//	成员邮箱
       'is_supervisor': True/False		//成员是否为管理员
      },
  	//……
   ]
  }
  ```

- 异常处理

  ```json
  {'errno': 2094, 'msg': "信息获取失败"}
  {'errno': 2093, 'msg': "团队不存在"}
  {'errno': 2092, 'msg': "无法获取团队信息"}
  {'errno': 2089, 'msg': "您不属于该团队"}
  ```

  