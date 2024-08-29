from django.db import models


# Province Model
class province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=255)

    def __str__(self):
        return self.province_name
    
# City Model
class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    province = models.ForeignKey('Province', on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name

