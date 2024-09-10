
from django.db import models
from django_ulid.models import ULIDField

   
class user_props(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    city = models.ForeignKey(
        city,
        on_delete=models.CASCADE,
    )

    # make user id as primary key
    id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)
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

