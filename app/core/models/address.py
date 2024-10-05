from django.db import models


# Province Model
class province(models.Model):
    province_id = models.IntegerField(primary_key=True)
    province_name = models.CharField(max_length=255)

    def __str__(self):
        return self.province_name


# City Model
class city(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=255)
    province = models.ForeignKey("Province", on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class district(models.Model):
    district_id = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=255)
    city = models.ForeignKey("City", on_delete=models.CASCADE)

    def __str__(self):
        return self.district_name


class sub_district(models.Model):
    subdistrict_id = models.IntegerField(primary_key=True)
    subdistrict_name = models.CharField(max_length=255)
    district = models.ForeignKey("District", on_delete=models.CASCADE)

    def __str__(self):
        return self.subdistrict_name


class postal_code(models.Model):
    postal_code_id = models.IntegerField(primary_key=True)
    subdistrict = models.ForeignKey("Sub_district", on_delete=models.CASCADE)
    district = models.ForeignKey("district", on_delete=models.CASCADE)
    city = models.ForeignKey("city", on_delete=models.CASCADE)
    province = models.ForeignKey("province", on_delete=models.CASCADE)
    post_code = models.CharField(max_length=255)

    def __str__(self):
        return self.post_code
