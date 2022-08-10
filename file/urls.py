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
    # path('project_root_filelist', views.project_root_filelist),
    path('get_dir_list', views.get_dir_list),
    path('delete_filelist_in_project', views.delete_filelist_in_project),
    path('get_my_filelist', views.get_my_filelist),
    path('project_root_uml_list', views.project_root_uml_list),
    path('project_root_doc_list', views.project_root_doc_list),
    path('project_root_pro_list', views.project_root_pro_list),
    path('create_team_file', views.create_team_file),
    path('get_file_centre_list', views.get_file_centre_list),
    path('delete_filelist_in_centre', views.delete_filelist_in_centre),
    path('completely_delete_file', views.completely_delete_file)
]
