# user/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('get_user_info', views.get_user_info),
    path('update_user_info', views.update_user_info),
    path('update_user_img', views.update_user_img),

]