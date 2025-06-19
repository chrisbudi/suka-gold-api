from django.urls import path, re_path
from .consumer import NotificationConsumer
from .views import api

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<user_id>\d+)/$", NotificationConsumer.as_asgi()),
]
