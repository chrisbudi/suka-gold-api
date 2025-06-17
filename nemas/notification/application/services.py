from typing import List
from interfaces.notification_sender import NotificationSender
from application.dto import NotificationDTO


class NotificationService:

    def __init__(self, senders: List[NotificationSender]):
        self.senders = senders

    def send_notification(self, notification: NotificationDTO):
        for sender in self.senders:
            sender.send(
                user=notification.user,
                title=notification.title,
                message=notification.message,
                data=notification.data,
            )
