from os import read
from attr import validate
from rest_framework import serializers
from ewallet.models import topup_transaction
from shared_kernel.services.external.xendit_service import qris_service
from user.models.users import user_virtual_account
from datetime import datetime, timedelta
from uuid import uuid4
import json


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
            # readonly field
            "topup_payment_channel_code",
            "topup_payment_number",
            "topup_payment_expires_at",
            "topup_payment_ref",
            "topup_payment_ref_code",
            "topup_transaction_id",
            "topup_timestamp",
            "topup_notes",
            "topup_status",
            "user",
        ]

        read_only_fields = [
            "topup_payment_channel_code",
            "topup_payment_number",
            "topup_payment_expires_at",
            "topup_payment_ref",
            "topup_payment_ref_code",
            "topup_transaction_id",
            "topup_timestamp",
            "topup_notes",
            "topup_status",
            "user",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if data["topup_total_amount"] != data["topup_admin"] + data["topup_amount"]:
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )
        return data

    def create(self, validated_data, **kwargs):
        user = self.context["request"].user  # Get the authenticated user
        validated_data["user"] = user

        qris = validated_data["topup_payment_method"]
        service = qris_service.QRISPaymentService()
        # Generate static VA
        payload = {
            "reference_id": f"qris_generated_user_{user.id}_{str(uuid4())}",
            "type": "DYNAMIC",
            "currency": "IDR",
            "amount": float(validated_data["topup_total_amount"]),
            "expired_at": (datetime.now() + timedelta(hours=2)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "channel_code": "ID_DANA",
            "is_closed": True,
        }
        payload_json = json.dumps(payload)
        qris = service.qris_payment_generate(payload_json)
        print(qris, "qris")
        # serializer.save(qris=qris, user=user)

        validated_data["topup_payment_method"] = "QRIS"
        validated_data["topup_payment_channel_code"] = qris.get("channel_code")
        validated_data["topup_payment_number"] = str(qris.get("id"))
        validated_data["topup_payment_expires_at"] = qris.get("expires_at")
        validated_data["topup_payment_ref"] = qris.get("reference_id")
        validated_data["topup_payment_ref_code"] = qris.get("qr_string")

        # topup_transaction.objects.create(**validated_data)

        self.context["response"] = {
            "total_amount": validated_data["topup_total_amount"],
            "qr_string": qris.get("qr_string"),
        }

        return super().create(validated_data, **kwargs)


class SimulatedPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = topup_transaction
        fields = [
            "amount",
        ]
