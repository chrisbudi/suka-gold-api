import email
import os
import random
from django import template
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from auth_core.models import email_otp
from shared.utils.notification import create_user_notification
from user.models.user_notification import (
    NotificationIconType,
    NotificationTransactionType,
)
from user.models import user
from django.dispatch import Signal
from user.signals import email_user_verification
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string

from user.models.users import user as User

from shared.services.email_service import EmailService


@receiver(email_user_verification)
def send_user_verification(sender, user: user, **kwargs):

    code = str(random.randint(100000, 999999))

    email_otp.objects.create(email=user.email, code=code)
    # Send email using SendGrid

    sendGridEmail = settings.SENDGRID_EMAIL

    mail = Mail(
        from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
        to_emails=[user.email],
        subject="Nemas OTP Code",
        plain_text_content=f"Your OTP code is: {code}. Please use this code to verify your email.",
    )

    mailService = EmailService()
    mailService.sendMail(mail)
    create_user_notification(
        user,
        title=f"Email Verification",
        message=f"A verification code has been sent to your email.",
        icon_type=NotificationIconType.INFO,
        transaction_type=NotificationTransactionType.EMAIL_VERIFICATION,
    )
