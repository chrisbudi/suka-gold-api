from django.db import models

from django.conf import settings
import uuid6
from core.fields.uuidv7_field import UUIDv7Field

# master config

# class master_gold_loan(models.Model):
#     """master gold loan"""
#     id=models.AutoField(primary_key=True)
#     pct_cost_admin=models.DecimalField(max_length=4,decimal_places=3)
#     pct_gold_min=models.DecimalField(max_length=4,decimal_places=3)

# gold_loan
class gold_loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    loan_datetime = models.DateTimeField(auto_created=True)
    loan_refnumber = models.CharField(max_length=255)
    loan_period_day = models.IntegerField()
    loan_add_extra_due_date = models.DateField()
    loan_add_extra_note = models.TextField()
    loan_due_date = models.DateField()
    loan_sa_gold_wgt = models.DecimalField(max_digits=8, decimal_places=4)
    loan_gold_wgt = models.DecimalField(max_digits=8,decimal_places=4)
    loan_gold_price_sell = models.DecimalField(max_digits=12,decimal_places=2)
    loan_amt = models.DecimalField(max_digits=16,decimal_places=2)
    loan_cost_admin = models.DecimalField(max_digits=12,decimal_places=2)
    total_loan_amt = models.DecimalField(max_digits=16,decimal_places=2)
    loan_status_id = models.IntegerField()
    loan_status_name=models.CharField(max_length=255)
    loan_last_payment_date=models.DateField()
    loan_total_payment_amt=models.DecimalField(max_digits=16,decimal_places=2)
    loan_note=models.TextField()
    update_time=models.DateTimeField(auto_now=True)
    update_user=models.CharField(max_length=255)
    create_time=models.DateTimeField(auto_created=True)
    create_user=models.CharField(max_length=255)    
     
    def __str__(self):
        return ""
    

# gold_loan_pay
# schedule payment last pay date

class gold_loan_pay(models.Model):
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    loan_id = models.ForeignKey(gold_loan,on_delete=models.CASCADE)
    loan_ref_number = models.CharField(max_length=255)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    loan_pay_timestamp = models.DateTimeField(auto_created=True)
    loan_pay_by = models.CharField(max_length=255)
    loan_last_due_date = models.DateField()
    loan_pay_no = models.CharField(max_length=255)
    loan_pay_ref_number = models.CharField(max_length=255)
    loan_pay_amount = models.DecimalField(max_digits= 16, decimal_places=2)
    loan_pay_status_id = models.IntegerField()
    loan_pay_status_name = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_created=True)
    create_user = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.CharField(max_length=255)
    def __str__(self):
        return self.id
    

    
