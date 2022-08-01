# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_team', views.create_team),
    path('invite_member', views.invite_member),
    path('kick_member', views.kick_member),
    path('set_manager', views.set_manager),
    path('get_team_info', views.get_team_info),

]
