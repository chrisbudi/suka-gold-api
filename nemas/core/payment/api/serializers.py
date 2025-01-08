"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import bank


# region Bank
class BankSerializer(serializers.ModelSerializer):
    """Serializer for bank object"""

    class Meta:
        model = bank
        fields = [
            "bank_id",
            "bank_name",
            "bank_code",
            "bank_logo_url",
            "bank_merchant_code",
            "bank_active",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "bank_id",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]


class BankFilter(filters.FilterSet):
    class Meta:
        model = bank

        fields = {
            "bank_code": ["icontains"],
        }


class BankUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value


# endregion
