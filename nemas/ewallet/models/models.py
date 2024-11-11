from django.db import models
from core.domain.address import city
from core.fields.uuidv7_field import UUIDv7Field


class user_props(models.Model):

    city = models.ForeignKey(
        city,
        on_delete=models.CASCADE,
    )

    # make user id as primary key
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    wallet_amt = models.DecimalField(max_digits=12, decimal_places=2)
    gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    invest_gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_amt = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    rek_number = models.CharField(max_length=255)
    npwp = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_post_code = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_created=True)
    create_user = models.CharField(max_length=255)
