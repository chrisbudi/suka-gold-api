from django.db import models
from app import settings
from core.fields import uuidv7_field


class BaseUserHistory(models.Model):
    id = uuidv7_field.UUIDv7Field(primary_key=True, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.date} - {self.note}"
