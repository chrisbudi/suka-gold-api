from celery import shared_task
from notification.application.services import NotificationService
from notification.application.dto import NotificationDTO


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def send_notification_task(self, dto_dict):
    dto = NotificationDTO(**dto_dict)
    NotificationService.send(dto)
