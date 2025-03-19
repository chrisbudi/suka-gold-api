from pickle import TRUE
from typing import Any
from django.db import models
from requests import delete


class payment_method(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    payment_method_name = models.CharField(max_length=50, unique=True)
    payment_method_description = models.CharField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_deleted = True
        self.save()
