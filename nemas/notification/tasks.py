from celery import shared_task
import logging

from application.services import NotificationService
from application.dto import NotificationDTO
from infrastructure.web_socket_sender import WebSocketSender

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_notification_task(self, user_id, title, message, data=None):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        ws_sender = WebSocketSender()

        service = NotificationService(senders=[ws_sender])

        notification = NotificationDTO(
            user=user, title=title, message=message, data=data or {}
        )
        service.send_notification(notification)

    except Exception as exc:
        logger.error(f"Error sending notification to user {user_id}: {str(exc)}")
        self.retry(exc=exc, countdown=min(2**self.request.retries * 60, 3600))
