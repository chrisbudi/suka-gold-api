from rest_framework import serializers
from wallet.models import topup_qris_webhook
from datetime import datetime


class PaymentDetailSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    source = serializers.CharField()


class TopupWebhookSerializer(serializers.Serializer):
    event = serializers.CharField()
    business_id = serializers.CharField()
    created = serializers.DateTimeField()

    data = serializers.DictField(child=serializers.JSONField())

    def validate(self, attrs):
        data = attrs.get("data", {})

        required_fields = ["id", "amount", "status", "currency", "qr_id"]
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(
                    f"Missing required field: {field} in data"
                )

        if data.get("currency") != "IDR":
            raise serializers.ValidationError("Only IDR currency is supported")

        if data.get("status") not in ["SUCCEEDED", "FAILED", "PENDING"]:
            raise serializers.ValidationError("Invalid payment status")

        return attrs


class QRISPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = topup_qris_webhook
        fields = "__all__"
        read_only_fields = ("created_at",)
