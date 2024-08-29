from django.db import models

class information_educational(models.Model):
    information_educational_id = models.AutoField(primary_key=True)
    information_name = models.CharField(max_length=255)
    information_notes = models.TextField(blank=True, null=True)
    information_url = models.URLField(max_length=200, blank=True, null=True)
    information_background = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.information_name


class information_customer_service(models.Model):
    information_customer_service_id = models.AutoField(primary_key=True)
    information_phone = models.CharField(max_length=20)
    information_name = models.CharField(max_length=255)

    def __str__(self):
        return self.information_name


class information_rating(models.Model):
    information_rate_id = models.AutoField(primary_key=True)
    information_rate_name = models.CharField(max_length=255)
    rate = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.information_rate_name
