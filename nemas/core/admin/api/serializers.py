"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import AdminFee, InvestmentReturn


class AdminFeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminFee
        fields = [
            "name",
            "fee_type",
            "value",
            "description",
        ]


class AdminFeeFilter(filters.FilterSet):

    class Meta:
        model = AdminFee

        fields = {
            "name": ["icontains"],
            "fee_type": ["exact"],
            "value": ["exact"],
        }
