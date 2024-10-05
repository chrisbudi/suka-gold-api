"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.models import (
    province,
    city,
    district,
    sub_district,
    postal_code,
)


# region Province
class ProvinceSerializer(serializers.ModelSerializer):
    """Serializer for Province service object"""

    class Meta:
        model = province
        fields = [
            "province_name",
            "province_id",
        ]
        read_only_fields = [
            "province_id",
        ]


class ProvinceFilter(filters.FilterSet):
    class Meta:
        model = province

        fields = {
            "province_name": ["icontains"],
        }


# endregion
