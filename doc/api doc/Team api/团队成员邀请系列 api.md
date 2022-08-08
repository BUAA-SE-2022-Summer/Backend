### 团队成员邀请系列 api

#### Invite_member(向某一用户发出邀请)：

  > 超管、普通管理员可以邀请成员加入团队，普通成员不可邀请

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
  
  {'errno': 2002, 'msg': "用户未登录"}
  {'errno': 2001, 'msg': "请求方式错误"}
  
  ```

#### Confirm_invitation(邮箱里的确认按钮跳转到的链接)

- 路由：/api/team/confirm_invitation

- GET

- url实例：

  > 前端把token返回给后端

  ```http
  http://127.0.0.1:8000/api/team/confirm_invitation?token=eyJ1c2VySUQiOjMxLCJlbWFpbCI6IjE1OTk3NjM3MzFAcXEuY29tIiwidGVhbUlEIjoxMSwiaW52aXRvcklEIjoxfQ.Yuv5Xw.FMk0zSWoCC1jrVdMUrh7zFv1lWo
  ```

- 后端返回格式：

  ```json
  {
      "errno": 0,
      "msg": "token解析成功",
      "teamID": 11,			//团队ID
      "invitorID": 1,		//邀请者ID
      "userID": 31			//被邀请者ID
  }		
  //以下为修改后的返回格式
  {
      "errno": 0,
      "msg": "token解析成功",
      "teamID": 11,
      "team_name": "teamLiver",
      "invitorID": 1,
      "invitor_name": "HR_TEST",
      "invitor_avatar": "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1.jpg",		//邀请者的头像的地址
      "userID": 31,
      "username": "Vera_email_test",
      "user_avatar": "xxxx	"																											//被邀请者的头像地址
  }
  ```

- 异常

  ```json
  {'errno': 2085, 'msg': "无法获取token信息"}
  {'errno': 2095, 'msg': "无法获取用户信息"}
  {'errno': 2092, 'msg': "无法获取团队信息"}
  {'errno': 2084, 'msg': "无法获取邀请人信息"}
  {'errno': 2001, 'msg': "请求方式错误"}
  ```

  

#### Accept_invitation（用户接受邀请）

  > 超管、普通管理员可以邀请成员加入团队，普通成员不可邀请

- 路由：/api/team/accept_invitation

- POST

- 前端请求格式

  ```json
  {
   'token':xxx,		//从邀请链接里扒拉下来的token
  }
  ```

- 后端返回格式

  ```json
  'errno': 0, 'msg': "您已成功加入团队" + team.team_name}
  ```

- 异常处理

  ```json
  {'errno': 2096, 'msg': "信息获取失败"}
  {'errno': 2095, 'msg': "无法获取用户信息"}
  {'errno': 2092, 'msg': "无法获取团队信息"}
  {'errno': 2086, 'msg': "无法获取邀请者信息"}
  {'errno': 2084, 'msg': "您已是团队" + team.team_name + '的成员'}
  {'errno': 2001, 'msg': "请求方式错误"}
  ```

