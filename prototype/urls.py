from django.urls import path
from . import views

urlpatterns = [
    path('create_prototype', views.create_prototype),
    path('delete_prototype', views.delete_prototype),
    path('create_page', views.create_page),
    path('open_prototype', views.open_prototype),
    path('change_page', views.change_page),
    path('change_page_name', views.change_page_name),
    path('update_page', views.update_page),
    path('delete_page', views.delete_page),
    path('share_prototype', views.share_prototype),
    path('enter_sharing_link', views.enter_sharing_link),
    path('close_sharing', views.close_sharing),
    path('change_page_when_sharing', views.change_page_when_sharing)
]
