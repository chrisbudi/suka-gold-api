import uuid
from django.db import models
from django.utils.timezone import now, timedelta
from django.conf import settings

from user.signals import (
    email_user_reset_token_done,
    email_user_reset_token,
)

from user.models import user_address


class user_reset_token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reset_tokens"
    )
    token = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    TYPE_CHOICES = [
        ("Password", "Reset Password"),
        ("Pin", "Reset PIN"),
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="Password")
    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    def is_valid(self):
        return now() < self.expires_at

    def send_reset_email(self, email_type):
        """Emit the password reset requested signal."""
        print(email_type, "email type")
        email_user_reset_token.send(
            sender=self.__class__,
            user=self.user,
            reset_key=str(self.token),
            email_type=email_type,
        )

    def send_reset_email_done(self, email_type):
        """Emit the password reset requested signal."""
        email_user_reset_token_done.send(
            sender=self.__class__, user=self.user, email_type=email_type
        )

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
