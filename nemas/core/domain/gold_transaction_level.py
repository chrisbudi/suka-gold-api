from django.db import models


class gold_transaction_level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    amount_min = models.CharField(max_length=50, unique=True)
    amount_max = models.BooleanField(default=False)
    benefit_a = models.BooleanField(default=True)
    benefit_b = models.BooleanField(default=True)
    benefit_c = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_deleted = True
        self.save()
