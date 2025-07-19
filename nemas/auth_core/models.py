# models.py
from django.db import models
from django.utils import timezone
from django_otp.plugins.otp_totp.models import TOTPDevice
import uuid


class email_otp(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    session_token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300


# implement TOTPDevice for 2FA
class TwoFactorAuthDevice(TOTPDevice):
    """
    Custom TOTP device for two-factor authentication.
    Inherits from django_otp's TOTPDevice.
    """

    class Meta:
        verbose_name = "Two Factor Auth Device"
        verbose_name_plural = "Two Factor Auth Devices"

    def __str__(self):
        return f"{self.name} ({self.user})"
