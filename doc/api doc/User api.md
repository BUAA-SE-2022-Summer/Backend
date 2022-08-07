# User api

#### register(注册)

- 路由：/api/user/register

- 请求方式：POST

- 前端request格式：

  ```json
  {
  'username':xxx,
  'password':xxx,
  'password_confirm':xxx,
  'real_name':xxx(可空),
  'email':xxx,
  'phone':xxx(可空),
  'profile':xxx(可空)
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '注册成功', 'level': 'above middle'}
  {'errno': 200, 'msg': "注册成功", 'level': 'strong'}
  ```
  
- 错误提示

  - 昵称为空

    ```json
    {'errno': 1, 'msg': '昵称不能为空'}
    ```

  - 密码为空

    ```json
    {'error': 2, 'msg': '密码不能为空'}
    ```

  - 确认密码为空

    ```json
    {'errno': 3, 'msg': '确认密码不能为空'}
    ```

  - 邮箱为空

    ```json
    {'errno': 4, 'msg': '邮箱不能为空'}
    ```
  
  - 邮箱格式错误
  
    ```json
    {'errno': 5, 'msg': '邮箱格式错误'}
    ```
  
  - 手机号格式错误
  
    ```json
    {'errno': 6, 'msg': '手机号格式错误'}
    ```
  
  - 昵称已存在
  
    ```json
    {'errno': 7, 'msg': "昵称已存在"}
    ```
  
  - 密码不一致
  
    ```json
    {'errno': 8, 'msg': '两次密码不一致'}
    ```
    
  - 密码校验
  
    ```json
    {'errno': 11, 'msg': '密码长度不能小于8位'}
    {'errno': 12, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'weak'}
    {'errno': 13, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'below middle'}
    {'errno': 14, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'middle'}
    {'errno': 15, 'msg': '密码包含非法字符'}
    ```
    
  - 请求方式错误
  
    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

#### login（登陆）

- 路由：/api/user/login

- 请求方式：POST

- 前端request格式：

  ```json
  {
  'username':xxx,
  'password':xxx
  }
  ```

- 后端response:

  ```json
  {
  'errno': 0, 
  'msg': "登录成功"
  }
  ```

- 错误提示

  - 昵称为空

    ```json
    {'errno': 1, 'msg': '昵称不能为空'}
    ```

  - 密码为空

    ```json
    {'errno': 2, 'msg': '密码不能为空'}
    ```

  - 密码错误

    ```json
    {'errno': 3, 'msg': "密码错误"}
    ```

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户不存在

    ```json
    {'errno': 1001, 'msg': '用户不存在'}
    ```

#### logout(登出)

- 路由：/api/user/logout

- 请求方式：GET

- 前端request格式：

  无

- 后端response:

  ```json
  {'errno': 0, 'msg': "注销成功"}
  ```

- 错误提示

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  - 用户未登录就登出

    ```json
    {'errno': 1002, 'msg': "未登录不能登出"}
    ```


#### get_user_info(获取用户基本信息)

- 路由：/api/user/get_user_info

- 请求方式：GET

- 前端request格式：

  无

- 后端response:

  ```json
  {
  'errno': 0, 
  'msg': "查询成功",
  'data':{
      'username': xxx, 
      'password':xxx,
      'real_name': xxx, 
      'email': xxx,
      'phone': xxx, 
      'profile': xxx,
      'img':xxx
  	}
  }
  ```

- 错误提示

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  -  用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能获取用户信息"}
    ```

#### update_user_info(修改用户基本信息)

- 路由：/api/user/update_user_info

- 请求方式：POST

- 前端request格式：

  ```json
  {
  'username':xxx,
  'password':xxx,
  'real_name':xxx,
  'email':xxx,
  'phone':xxx,
  'profile':xxx
  }
  ```

- 后端response:

  ```json
  {'errno': 0, 'msg': '修改用户信息成功', 'level': 'above middle'}
  {'errno': 200, 'msg': "修改用户信息成功", 'level': 'strong'}
  ```

- 错误提示

  - 邮箱格式错误

    ```json
    {'errno': 1, 'msg': '邮箱格式错误'}
    ```

  - 手机号格式错误

    ```json
    {'errno': 2, 'msg': '手机号格式错误'}
    ```
  
  - 昵称为空
  
    ```json
    {'errno': 3, 'msg': '昵称不能为空'}
    ```
  
  - 密码为空
  
    ```json
    {'errno': 4, 'msg': '密码不能为空'}
    ```
  
  - 密码校验
  
    ```json
    {'errno': 11, 'msg': '密码长度不能小于8位'}
    {'errno': 12, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'weak'}
    {'errno': 13, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'below middle'}
    {'errno': 14, 'msg': '密码必须包含数字、字母大小写、特殊字符中三种', 'level': 'middle'}
    {'errno': 15, 'msg': '密码包含非法字符'}
    ```
  
  - 请求方式错误
  
    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```
  
  -  用户未登录
  
    ```json
    {'errno': 1002, 'msg': "未登录不能修改用户信息"}
    ```

#### update_user_img(获取用户基本信息)

- 路由：/api/user/update_user_img

- 请求方式：POST

- 前端request格式：

  ```
  {
  img:xxx(File类型)
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0, 
      'msg': "修改用户头像成功",
      'url': img_url
  }
  ```

- 错误提示

  - 请求方式错误

    ```json
    {'errno': 10, 'msg': "请求方式错误"}
    ```

  -  用户未登录

    ```json
    {'errno': 1002, 'msg': "未登录不能修改用户头像"}
    ```

















