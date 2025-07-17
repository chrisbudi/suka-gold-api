# models.py
from django.db import models
from django.utils import timezone
import uuid


class email_otp(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    session_token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300
