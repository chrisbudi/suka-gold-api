import uuid
from django.db import models
from django.utils.timezone import now, timedelta
from .users import user

from user.signals import email_user_reset_password, email_user_reset_password_done


class user_reset_token(models.Model):
    user = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="reset_tokens"
    )
    token = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    TYPE_CHOICES = [
        ("reset_password", "Reset Password"),
        ("reset_pin", "Reset PIN"),
    ]
    type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default="reset_password"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=now() + timedelta(hours=24)
    )  # Token valid for 24 hour

    def is_valid(self):
        return now() < self.expires_at

    # def send_reset_pin_email(self):
    #     """Emit the PIN reset requested signal."""
    #     email_user_reset_pin.send(
    #         sender=self.__class__, user=self.user, token=self.token
    #     )

    # def send_reset_pin_email_done(self):
    #     """Emit the PIN reset requested signal."""
    #     email_user_reset_pin_done.send(sender=self.__class__, user=self.user)

    def send_reset_password_email(self, request):
        """Emit the password reset requested signal."""
        print("send_reset_password_email produce", self.user, self.token)
        email_user_reset_password.send(
            sender=self.__class__, user=self.user, reset_key=str(self.token)
        )

    def send_reset_password_email_done(self):
        """Emit the password reset requested signal."""
        email_user_reset_password_done.send(sender=self.__class__, user=self.user)
