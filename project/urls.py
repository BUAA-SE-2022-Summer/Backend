from django.urls import path
from . import views


urlpatterns = [
    path('create_project', views.create_project),
    path('delete_project', views.delete_project),
    path('star_project', views.star_project),
    path('unstar_project', views.unstar_project),
    path('rename_project', views.rename_project),
    path('get_project_list', views.get_project_list),
    path('get_star_project_list', views.get_star_project_list),
    path('get_create_project_list', views.get_create_project_list),
    path('get_delete_project_list', views.get_delete_project_list),
    path('delete_project_recycle_bin', views.delete_project_recycle_bin),
    path('cancel_delete_project', views.cancel_delete_project),
]
