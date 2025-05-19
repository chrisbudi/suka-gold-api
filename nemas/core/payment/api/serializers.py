"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import bank as Bank
from datetime import datetime
from core.domain.payment import payment_method


# region Payment Method
class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for bank object"""

    class Meta:
        model = payment_method
        fields = [
            "payment_method_id",
            "payment_method_name",
            "payment_method_description",
            "is_active",
        ]
        read_only_fields = []


class PaymentMethodFilter(filters.FilterSet):
    class Meta:
        model = payment_method

        fields = {
            "payment_method_name": ["icontains"],
        }


# endregion


# region Bank
class BankSerializer(serializers.ModelSerializer):
    """Serializer for bank object"""

    class Meta:
        model = Bank
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

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user.id
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user.id
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user.id
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class BankFilter(filters.FilterSet):
    class Meta:
        model = Bank

        fields = {
            "bank_merchant_code": ["icontains"],
            "bank_name": ["icontains"],
            "bank_active": ["exact"],
        }


class BankUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 1 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 1MB")
        return value


# endregion
