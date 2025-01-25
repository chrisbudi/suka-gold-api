from attr import validate
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
            "topup_payment_method",
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

    def save(self, **kwargs):
        print(kwargs, "kwargs")
        super().save(**kwargs)
        # return None

    def create(self, validated_data, **kwargs):
        print(self.context.get("qris"), self.context.get("user"), kwargs, "kwargs")
        qris = self.context.get("qris")
        user = self.context.get("user")

        print(qris, "qris", user, "user")
        # validated_data["topup_payment_method"] = "QRIS"
        # validated_data["topup_payment_channel_code"] = kwargs.get("channel_code")
        # validated_data["topup_payment_number"] = kwargs.get("id")

        # validated_data["topup_payment_expires_at"] = kwargs.get("expires_at")
        # validated_data["topup_payment_ref"] = kwargs.get("reference_id")
        # validated_data["topup_payment_ref_code"] = kwargs.get("qr_string")
        # print(validated_data, "validated_data")
        return None
        return topup_transaction.objects.create(**validated_data)


class SimulatedPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = topup_transaction
        fields = [
            "amount",
        ]
