import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
from notification.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
print("ASGI application is starting...")

application = (
    ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": OriginValidator(
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
                [
                    "null",
                    "localhost",
                    "http://www.nemas.id",
                    "https://www.nemas.id/",
                ],
            ),
        },
    ),
)
