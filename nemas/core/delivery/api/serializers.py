"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import (
    delivery_partner,
    delivery_partner_service,
)


# region Postal Code
class DeliveryPartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = delivery_partner
        fields = [
            "delivery_partner_id",
            "delivery_partner_name",
            "delivery_partner_code",
            "delivery_partner_description",
            "is_deleted",
        ]


class DeliveryPartnerFilter(filters.FilterSet):

    class Meta:
        model = delivery_partner

        fields = {
            "delivery_partner_code": ["icontains"],
        }


# endregion


# region Postal Code
class DeliveryPartnerServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = delivery_partner_service
        fields = [
            "delivery_partner_service_id",
            "delivery_partner_service_name",
            "delivery_partner",
            "delivery_partner_service_code",
            "delivery_partner_service_description",
        ]


class DeliveryPartnerServiceFilter(filters.FilterSet):

    class Meta:
        model = delivery_partner_service

        fields = {
            "delivery_partner_service_code": ["icontains"],
        }


# endregion
