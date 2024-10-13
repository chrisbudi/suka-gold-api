"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import (
    province,
    city,
    district,
    subdistrict,
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


# region City
class CitySerializer(serializers.ModelSerializer):
    """Serializer for Province service object"""

    province_name = serializers.CharField(
        source="province.province_name", read_only=True
    )

    class Meta:
        model = city
        fields = [
            "city_name",
            "province_name",
        ]
        read_only_fields = [
            "city_id",
        ]


class CityFilter(filters.FilterSet):
    class Meta:
        model = city

        fields = {
            "city_name": ["icontains"],
        }


# endregion


# region District
class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for city object"""

    city_name = serializers.CharField(source="city.city_name", read_only=True)

    class Meta:
        model = district
        fields = [
            "district_name",
            "city_name",
        ]
        read_only_fields = ["district_id"]


class DistrictFilter(filters.FilterSet):
    class Meta:
        model = district
        fields = {
            "district_name": ["icontains"],
        }


# endregion


# region sub District
class SubDistrictSerializer(serializers.ModelSerializer):
    """Serializer for city object"""

    district_name = serializers.CharField(
        source="district.district_name", read_only=True
    )

    class Meta:
        model = subdistrict
        fields = [
            "subdistrict_name",
            "district_name",
        ]
        read_only_fields = [
            "subdistrict_id",
        ]


class SubDistrictFilter(filters.FilterSet):
    class Meta:
        model = subdistrict

        fields = {
            "subdistrict_name": ["icontains"],
        }


# endregion


# region Postal Code
class PostalCodeSerializer(serializers.ModelSerializer):
    """Serializer for city object"""

    district_name = serializers.CharField(
        source="district.district_name", read_only=True
    )

    subdistrict_name = serializers.CharField(
        source="subdistrict.subdistrict_name", read_only=True
    )

    city_name = serializers.CharField(source="city.city_name", read_only=True)

    province_name = serializers.CharField(
        source="province.province_name", read_only=True
    )

    class Meta:
        model = postal_code
        fields = [
            "post_code",
            "district_name",
            "subdistrict_name",
            "city_name",
            "province_name",
            "district_id",
            "subdistrict_id",
            "city_id",
            "province_id",
        ]
        read_only_fields = [
            "postal_code_id",
        ]


class PostalCodeFilter(filters.FilterSet):

    district_name = serializers.CharField(
        source="district.district_name", read_only=True
    )

    subdistrict_name = serializers.CharField(
        source="subdistrict.subdistrict_name", read_only=True
    )

    city_name = serializers.CharField(source="city.city_name", read_only=True)

    province_name = serializers.CharField(
        source="province.province_name", read_only=True
    )

    class Meta:
        model = postal_code

        fields = {
            "post_code": ["icontains"],
        }


# endregion
