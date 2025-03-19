from django.db import models


class delivery_partner(models.Model):
    delivery_partner_id = models.AutoField(primary_key=True)
    delivery_partner_name = models.CharField(max_length=50, unique=True)
    delivery_partner_description = models.CharField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()


class delivery_partner_service(models.Model):
    delivery_partner_service_id = models.AutoField(primary_key=True)
    delivery_partner_service_name = models.CharField(max_length=50, unique=True)
    delivery_partner_service_code = models.CharField(max_length=50, unique=True)
    delivery_partner_service_description = models.CharField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()


class delivery_shipment_content(models.Model):
    delivery_partner_id = models.ForeignKey(
        "delivery_partner", on_delete=models.CASCADE, null=True
    )
    shipment_type_code = models.CharField(max_length=50)
    shipment_content_code = models.CharField(max_length=50)
    shipment_content_name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()


class delivery_partner_district(models.Model):
    delivery_partner_id = models.ForeignKey(
        "delivery_partner", on_delete=models.CASCADE, null=True
    )
    city_code = models.CharField(max_length=50)
    district_code = models.CharField(max_length=50, null=True)
    district_name = models.CharField(max_length=150, null=True)
    zone_code = models.CharField(max_length=50, null=True)
    provinsi_code = models.CharField(max_length=50, null=True)
    city_name = models.CharField(max_length=50, null=True)
    tlc_branch_code = models.CharField(max_length=50)
    province_name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()
