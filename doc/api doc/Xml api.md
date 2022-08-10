# Xml api

#### get_user_xml(获取用户xml文件列表)

- 路由：/api/file/get_user_xml

- 请求方式：POST

- 前端request格式：

  ```json
  {
  	
  }
  ```

- 后端response:

  ```json
  {
      'errno': 0, 
      'msg': "成功获取用户xml文件", 
      'xml_list': [
          {
              'xmlID': xxx,
              'xml_name': xxx,
              'content': xxx,
              'last_modify_time': xxx,
          }
          ……
      ]
  }
  ```

- 错误提示

  ```json
  //请求方式错误
  {'errno': 3001, 'msg': "请求方式错误"}
  //用户未登录
  {'errno': 3002, 'msg': "用户未登录"}
  ```

  #### update_xml(更新xml文件)

  - 路由：/api/file/update_xml

  - 请求方式：POST

  - 前端request格式：

    ```json
    {
    	'xmlID':xxx,
        'content':xxx,
    }
    ```

  - 后端response:

    ```json
    {'errno': 0, 'msg': "成功更新xml文件"}
    ```

  - 错误提示

    ```json
    //请求方式错误
    {'errno': 3001, 'msg': "请求方式错误"}
    //用户未登录
    {'errno': 3002, 'msg': "用户未登录"}
    {'errno': 3094, 'msg': "信息获取失败"}
    {'errno': 3098, 'msg': "xml文件不存在"}
    ```

    #### save_xml(保存xml文件)

    - 路由：/api/file/save_xml

    - 请求方式：POST

    - 前端request格式：

      ```json
      {
      	'xml_name':xxx,
          'content':xxx,
      }
      ```

    - 后端response:

      ```json
      {'errno': 0, 'msg': "成功保存xml文件"}
      ```

    - 错误提示

      ```json
      //请求方式错误
      {'errno': 3001, 'msg': "请求方式错误"}
      //用户未登录
      {'errno': 3002, 'msg': "用户未登录"}
      {'errno': 3094, 'msg': "信息获取失败"}
      {'errno': 3099, 'msg': "xml文件名称不得为空"}
      {'errno': 3102, 'msg': "xml文件名称重复"}
      ```

      #### delete_xml(删除xml文件)

      - 路由：/api/file/delete_xml

      - 请求方式：POST

      - 前端request格式：

        ```json
        {
        	'xmlID':xxx,
        }
        ```

      - 后端response:

        ```json
        {'errno': 0, 'msg': "成功删除xml文件"}
        ```

      - 错误提示

        ```json
        //请求方式错误
        {'errno': 3001, 'msg': "请求方式错误"}
        //用户未登录
        {'errno': 3002, 'msg': "用户未登录"}
        {'errno': 3094, 'msg': "信息获取失败"}
        {'errno': 3098, 'msg': "xml文件不存在"}
        ```

        
