# user/urls.py
from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    # path('create_team', views.create_team),
    path('create_file', views.create_file),
    path('edit_file', views.edit_file),
    path('read_file', views.read_file),
    path('delete_file', views.delete_file),
    path('restore_file', views.restore_file),
    path('project_root_filelist', views.project_root_filelist),
    path('get_dir_list', views.get_dir_list),
    path('delete_filelist',views.delete_filelist_in_project)
]
