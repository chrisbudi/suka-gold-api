from .dto import NotificationDTO
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationService:
    @staticmethod
    def send(dto: NotificationDTO):
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(
                f"user_{dto.user_id}",
                {
                    "type": "send_notification",
                    "title": dto.title,
                    "message": dto.message,
                    "data": dto.data,
                },
            )
