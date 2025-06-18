from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger(__name__)


from typing import Optional


def send_ws_notification(
    user_id: int, title: str, message: str, data: Optional[dict] = None
):
    """
    Global WebSocket notification sender
    """
    try:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(
                f"user_{user_id}",
                {
                    "type": "send_notification",
                    "title": title,
                    "message": message,
                    "data": data or {},
                },
            )
        else:
            logger.error(
                "No channel layer available. Cannot send WebSocket notification."
            )
    except Exception as e:
        logger.error(f"WebSocket send failed for user {user_id}: {e}")
