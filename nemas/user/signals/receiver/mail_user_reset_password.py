import os
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from user.models import user
from django.dispatch import Signal
from user.signals import email_user_reset_password, email_user_reset_password_done


@receiver(email_user_reset_password)
def send_reset_password_email(sender, user: user, reset_key: str, **kwargs):
    print("send_reset_password_email consume", user, reset_key)
    # Load email template
    template_path = os.path.join(
        settings.BASE_DIR, "app", "templates", "email", "user", "reset_password.txt"
    )

    with open(template_path, "r") as template_file:
        email_body = template_file.read()

    # Format the email body with the reset key
    reset_link = f"{settings.EMAIL_SITE_URL}/reset-password/{reset_key}/"
    email_body = email_body.format(
        user_name=user.name,
        reset_link=reset_link,
    )

    # Send the email
    send_mail(
        subject="Password Reset Request",
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
    )


@receiver(email_user_reset_password_done)
def send_reset_password_email_done(sender, user: user, **kwargs):
    # Load email template
    template_path = os.path.join(
        settings.BASE_DIR,
        "app",
        "templates",
        "email",
        "user",
        "reset_password_done.txt",
    )

    with open(template_path, "r") as template_file:
        email_body = template_file.read()

    email_body = email_body.format(
        user_name=user.name,
    )

    # Send the email
    send_mail(
        subject="Password Reset Request",
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
    )
