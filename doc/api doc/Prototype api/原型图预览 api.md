### 原型图预览 api

#### share_prototype（获取分享加密串）

- 路由：/api/prototype/share_prototype

- 请求方式：POST

- 前端request格式

  ```json
  {
  'prototypeID':xxx,
  }
  ```

- 后端返回格式

  ```json
  {
      "errno": 0,
      "msg": "成功获取加密串",
      "code": "eyJwcm9JRCI6IjEwIn0.YvC93g.h1HLdUsisQVthaq1Orf6kzYAdSs"
  }
  ```

- 异常

  ```json
  {'errno': 10, 'msg': '请求方式错误'}
  {'errno': 1002, 'msg': "请先登录"}
  {'errno': 4, 'msg': '信息获取失败'}
  {'errno': 1, 'msg': '您不具有分享权限'}
  
  ```

#### enter_sharing_link（进入预览界面）

- 路由：/api/prototype/enter_sharing_link

- 请求方式：POST

- 前端request格式

  ```json
  {
  'code':xxx,		//链接里的加密串
  }
  ```

- 后端返回格式

  ```json
  {
      'errno': 0,
      'msg': '正在进入预览界面',
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

- 异常

  ```json
  {'errno': 10, 'msg': '请求方式错误'}
  {'errno': 1002, 'msg': "请先登录"}
  {'errno': 4, 'msg': '信息获取失败'}
  {'errno': 5, 'msg': '原型图预览未开启'}
  ```

#### close_sharing（关闭分享）

- 路由：/api/prototype/sclose_sharing

- 请求方式：POST

- 前端request格式

  ```json
  {
  'prototypeID':xxx,
  }
  ```

- 后端返回格式

  ```json
  {
      "errno": 0,
      "msg": "成功获取加密串",
      "code": "eyJwcm9JRCI6IjEwIn0.YvC93g.h1HLdUsisQVthaq1Orf6kzYAdSs"
  }
  ```

- 异常

  ```json
  {'errno': 1002, 'msg': "请先登录"}
  {'errno': 10, 'msg': '请求方式错误'}
  {'errno': 6, 'msg': '预览功能已关闭'}
  {'errno': 4, 'msg': '信息获取失败'}
  {'errno': 1, 'msg': '您不具有分享权限'}
  
  ```

#### change_page_when_sharing（关闭分享）

- 路由：/api/prototype/change_page_when_sharing

- 请求方式：POST

- 前端request格式

  ```json
  {
  'code':xxx,
  'pageID':xxx
  }
  ```

- 后端返回格式

  ```json
  {'errno': 0,
   'msg': '打开页面'+page.pageName,
   'componentData': componentData,
   'canvasStyle': page.pageCanvasStyle,
  }
  ```

- 异常

  ```json
  {'errno': 10, 'msg': '请求方式错误'}
  {'errno': 5, 'msg': '预览功能已关闭，无法打开页面'}
  {'errno': 4, 'msg': '信息获取失败'}
  
  ```


