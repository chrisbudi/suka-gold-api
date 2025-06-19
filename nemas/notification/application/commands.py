from notification.application.dto import NotificationDTO
from notification.application.services import NotificationService
from notification.tasks import send_notification_task


def notify_user(dto: NotificationDTO):
    send_notification_task.delay(dto.__dict__)
