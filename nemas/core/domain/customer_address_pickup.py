from django.db import models


class customer_address_pickup(models.Model):
    customer_address_pickup_id = models.IntegerField(primary_key=True)
    customer_address_pickup_address = models.CharField(max_length=255)
    customer_address_pickup_name = models.CharField(max_length=255)
