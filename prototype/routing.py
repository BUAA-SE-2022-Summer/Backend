from django.urls import path
from prototype.consumers import Editprototype

websocket_urlpatterns = [
    path('edit_prototype', Editprototype.as_asgi()),
]