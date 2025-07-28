"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import AdminFee, InvestmentReturn


class InvestmentReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentReturn
        fields = [
            "id",
            "name",
            "rate",
            "duration_days",
            "description",
        ]


class InvestmentReturnServiceFilter(filters.FilterSet):

    class Meta:
        model = InvestmentReturn

        fields = {
            "name": ["icontains"],
            "rate": ["exact"],
            "duration_days": ["exact"],
            "description": ["icontains"],
        }


# endregion
