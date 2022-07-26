# user/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('find_all', views.find_all),
]