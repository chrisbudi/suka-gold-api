from application.dto import NotificationDTO
from application.services import NotificationService


class SendNotificationCommand:

    def __init__(self, service: NotificationService):
        self.service = service

    def execute(self, user, title, message, data=None):
        notification = NotificationDTO(
            user=user, title=title, message=message, data=data
        )
        self.service.send_notification(notification)
