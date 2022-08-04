EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 指定邮件后端
EMAIL_HOST = 'smtpdm.aliyun.com'  # 发邮件主机
EMAIL_PORT = 465  # 发邮件端口
EMAIL_HOST_USER = 'mobook@horik.cn'  # 授权的邮箱
EMAIL_HOST_PASSWORD = '2022LiverTeam'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '墨书<mobook@horik.cn>'  # 发件人抬头

# html_message = '<p>尊敬的用户您好！</p>' \
#                        '<p>感谢您使用商城。</p>' \
#                        '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
#                        '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)   # verify_url是验证路由
