from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification.interfaces.notification_sender import NotificationSender


class WebSocketSender(NotificationSender):

    def send(self, user, title: str, message: str, data: dict):
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "title": title,
                    "message": message,
                    "data": data or {},
                },
            )
        else:
            # Optionally, log or handle the error here
            pass
