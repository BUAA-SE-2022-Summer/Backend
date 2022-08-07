from django.urls import path
from prototype.consumers import Editprototype

websocket_urlpatterns = [
    path('edit_prototype/<int:pageID>', Editprototype.as_asgi()),
]