import email
import os
from django import template
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from shared.utils.notification import create_user_notification
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from user.models import user
from django.dispatch import Signal
from user.signals import email_user_reset_token_done, email_user_reset_token
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string

from user.models.users import user as User

from shared.services.email_service import EmailService


@receiver(email_user_reset_token)
def send_reset_password_email(
    sender, user: user, reset_key: str, email_type=str, **kwargs
):

    mail = generate_email(user, reset_key, str(email_type))
    if mail:

        mailService = EmailService()
        mailService.sendMail(mail)
        create_user_notification(
            user,
            title=f"{email_type} Reset Request",
            message=f"Permintaan reset {email_type} telah dikirim ke email Anda.",
            icon_type=NotificationIconType.INFO,
            transaction_type=NotificationTransactionType.FORGOT_PASSWORD,
        )
    else:
        print("Failed to generate email. Mail object is None.")


def generate_email(user: User, reset_key: str, email_type: str):
    # Format the email body with the reset key
    reset_link = f"{settings.EMAIL_SITE_URL}/{'reset-pin' if email_type == 'PIN' else 'reset-password'}/{reset_key}/"
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/user/reset_pin_password.html",
            {
                "NAMA_USER": user.name,
                "Password_PIN": email_type,
                "URL_RESET_PASSWORD_PIN": reset_link,
                **mail_props,
            },
        )

        sendGridEmail = settings.SENDGRID_EMAIL
        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject=f"{email_type} Reset Request",
            html_content=email_html,
        )
        return message
    except Exception as e:
        print(e)


@receiver(email_user_reset_token_done)
def send_reset_password_email_done(sender, user: user, email_type: str, **kwargs):
    mail = generate_email_done(user, str(email_type))
    if mail:

        mailService = EmailService()
        mailService.sendMail(mail)
        create_user_notification(
            user,
            title=f"{email_type} Reset Request",
            message=f"{email_type} reset telah berhasil.",
            icon_type=NotificationIconType.INFO,
            transaction_type=NotificationTransactionType.FORGOT_PASSWORD,
        )
    else:
        print("Failed to generate email. Mail object is None.")


def generate_email_done(user: User, email_type: str):
    # Format the email body with the reset key
    mail_props = EmailService().get_email_props()
    try:
        email_html = render_to_string(
            "email/user/reset_pin_password_done.html",
            {
                "NAMA_USER": user.name,
                "Password_PIN": email_type,
                **mail_props,
            },
        )

        sendGridEmail = settings.SENDGRID_EMAIL
        message = Mail(
            from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
            to_emails=[user.email],
            subject=f"{email_type} Reset Done Confirmation",
            html_content=email_html,
        )
        return message
    except Exception as e:
        print(e)
