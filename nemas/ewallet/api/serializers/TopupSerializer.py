from rest_framework import serializers
from ewallet.models import topup_transaction
from user.models.users import user_virtual_account


class TopupVASerializer(serializers.ModelSerializer):
    class Meta:
        model = topup_transaction
        fields = [
            "topup_total_amount",
            "topup_admin",
            "topup_amount",
            "topup_payment_bank",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if data["topup_total_amount"] != data["topup_admin"] + data["topup_amount"]:
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )
        return data

    def create(self, validated_data, userVa: user_virtual_account):
        validated_data["topup_status"] = "pending"
        validated_data["user"] = userVa.user
        validated_data["topup_payment_method"] = "virtual_account"
        validated_data["topup_payment_number"] = userVa.va_number
        return topup_transaction.objects.create(**validated_data)


class TopupQrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = topup_transaction
        fields = [
            "topup_total_amount",
            "topup_admin",
            "topup_amount",
            "topup_payment_method",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if data["topup_total_amount"] != data["topup_admin"] + data["topup_amount"]:
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )
        return data

    def create(self, validated_data, *args, **kwargs):
        validated_data["topup_status"] = "pending"
        validated_data["topup_payment_method"] = "qris"
        return topup_transaction.objects.create(**validated_data)


class SimulatedPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
