from django.urls import path
from file.consumers import EditFile

websocket_urlpatterns = [
    path('edit_file', EditFile.as_asgi()),
]
