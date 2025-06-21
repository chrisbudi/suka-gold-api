from django.utils.timezone import now as timezone_now

from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)


def create_user_notification(
    user,
    title,
    message,
    icon_type: NotificationIconType,
    transaction_type: NotificationTransactionType,
):
    """
    Create a user notification.

    Args:
        user: The user object to whom the notification belongs.
        title: The title of the notification.
        message: The content of the notification.
        type: The type of the notification (e.g., 'info', 'warning', 'error').
        is_read: Boolean indicating if the notification has been read.

    Returns:
        The created user notification object.
    """
    from user.models import user_notification

    return user_notification.objects.create(
        user=user,
        user_notification_title=title,
        user_notification_description=message,
        user_notification_icon_type=icon_type,
        user_notification_date=timezone_now(),
        user_notification_transaction_type=transaction_type,
        user_notification_transaction_id=None,
    )
