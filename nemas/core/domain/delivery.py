from django.db import models
import random


class delivery_partner(models.Model):
    delivery_partner_id = models.AutoField(primary_key=True)
    delivery_partner_name = models.CharField(max_length=50, unique=True)
    delivery_partner_description = models.CharField(max_length=50, unique=True)
