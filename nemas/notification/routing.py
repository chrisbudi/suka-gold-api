from django.urls import path, re_path
from .consumer import NotificationConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/notifications/(?P<user_id>[0-9a-fA-F\-]{36})/?$",
        NotificationConsumer.as_asgi(),
    ),
]
