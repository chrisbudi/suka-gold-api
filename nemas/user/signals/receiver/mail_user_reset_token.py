import email
import os
from django import template
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from user.models import user
from django.dispatch import Signal
from user.signals import email_user_reset_token_done, email_user_reset_token


@receiver(email_user_reset_token)
def send_reset_password_email(
    sender, user: user, reset_key: str, email_type=str, **kwargs
):
    print(email_type, "email type")

    template_file = "reset_pin.txt" if email_type == "PIN" else "reset_password.txt"
    reset_link = f"{settings.EMAIL_SITE_URL}/{'reset-pin' if email_type == 'PIN' else 'reset-password'}/{reset_key}/"
    template_path = os.path.join(
        settings.BASE_DIR, "app", "templates", "email", "user", template_file
    )
    with open(template_path, "r") as template_file:
        email_body = template_file.read()

    # Format the email body with the reset key
    email_body = email_body.replace("{user_name}", user.name).replace(
        "{reset_link}", f'<a href="{reset_link}">{reset_link}</a>'
    )

    # Send the email
    send_mail(
        subject=f"{email_type} Reset Request",
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
        html_message=email_body,
    )


@receiver(email_user_reset_token_done)
def send_reset_password_email_done(sender, user: user, email_type: str, **kwargs):
    # Load email template
    print(email_type, "email type")
    template_file = (
        "reset_pin_done.txt" if email_type == "PIN" else "reset_pin_done.txt"
    )

    template_path = os.path.join(
        settings.BASE_DIR,
        "app",
        "templates",
        "email",
        "user",
        template_file,
    )

    with open(template_path, "r") as template_file:
        email_body = template_file.read()

    email_body = email_body.format(
        user_name=user.name,
    )

    # Send the email
    send_mail(
        subject=f"{email_type} Reset Request Successful",
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
    )
