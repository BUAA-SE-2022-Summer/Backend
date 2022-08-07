from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import file.routing
import prototype.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            file.routing.websocket_urlpatterns + prototype.routing.websocket_urlpatterns
        )
    ),
})
