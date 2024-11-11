"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import (
    information_educational,
    information_promo,
    information_customer_service,
    information_rating,
)


# region Information Customer Service
class InformationCustomerServiceSerializer(serializers.ModelSerializer):
    """Serializer for information customer service object"""

    class Meta:
        model = information_customer_service
        fields = [
            "information_customer_service_id",
            "information_phone",
            "information_name",
        ]
        read_only_fields = [
            "information_customer_service_id",
        ]


class InformationCustomerServiceFilter(filters.FilterSet):
    class Meta:
        model = information_customer_service

        fields = {
            "information_name": ["icontains"],
        }


# endregion


# region Information Educational
class InformationEducationalSerializer(serializers.ModelSerializer):
    """Serializer for Information Educational object"""

    class Meta:
        model = information_educational
        fields = [
            "information_name",
            "information_notes",
            "information_url",
            "information_background",
        ]
        read_only_fields = [
            "information_educational_id",
        ]


class InformationEducationalServiceFilter(filters.FilterSet):
    class Meta:
        model = information_educational
        fields = {
            "information_name": ["icontains"],
            "information_background": ["icontains"],
        }


# endregion


# region Information Promo
class InformationPromoSerializer(serializers.ModelSerializer):
    """Serializer for information Promo object"""

    class Meta:
        model = information_promo
        fields = [
            "promo_code",
            "leveling_user",
            "promo_name",
            "promo_url",
            "promo_start_date",
            "promo_end_date",
            "promo_tag",
            "promo_url_background",
            "promo_diskon",
            "promo_cashback",
            "promo_cashback_tipe_user",
            "merchant_cashback",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "id_promo",
        ]


class InformationPromoFilter(filters.FilterSet):
    class Meta:
        model = information_promo

        fields = {
            "promo_code": ["icontains"],
            "promo_name": ["icontains"],
        }


# endregion


# region Information Rating
class InformationRatingSerializer(serializers.ModelSerializer):
    """Serializer for information Rating object"""

    class Meta:
        model = information_rating
        fields = ["information_rate_name", "rate", "message", "publish"]
        read_only_fields = [
            "information_rate_id",
        ]


class InformationRatingFilter(filters.FilterSet):
    class Meta:
        model = information_rating

        fields = {
            "information_rate_name": ["icontains"],
        }


# endregion
