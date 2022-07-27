### Preface

#### register(注册)

- 路由：/user/register

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

  - 用户名为空

    ```json
    {'errno': 1, 'msg': '用户名不能为空'}
    ```

  - 密码为空

    ```json
    {'errno': 2, 'msg': '密码不能为空'}
    ```

  - 用户名已存在

    ```json
    {'errno': 3, 'msg': "用户名已存在"}
    ```

  - 请求方式错误

    ```json
    {'errno': 4, 'msg': "请求方式错误"}
    ```

#### login（登陆）

- 路由：/user/login

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
  'msg': "注册成功"
  }
  ```

- 错误提示

  - 用户名为空

    ```json
    {'errno': 1, 'msg': '用户名不能为空'}
    ```

  - 密码为空

    ```json
    {'errno': 2, 'msg': '密码不能为空'}
    ```

  - 用户名已存在

    ```json
    {'errno': 3, 'msg': "密码错误"}
    ```

  - 请求方式错误

    ```json
    {'errno': 5, 'msg': "请求方式错误"}
    ```

  - 用户名不存在

    ```json
    {'errno': 1001, 'msg': '用户名不存在'}
    ```

#### Find_all(获取所有用户信息)

- 路由：/user/login

- 请求方式：**GET**

- 前端request格式：

  无

- 后端response:

  ```json
  {
  'errno': 0, 
  'msg': "查询成功",
  'data':[
    {"userID": xxx,
  	 "username": xxx},
    {"userID": xxx,
  	 "username": xxx},
    ……
  ]
  }
  ```

- 错误提示

  - 请求方式错误

    ```json
    {'errno': 5, 'msg': "请求方式错误"}
    ```

  

#### 

