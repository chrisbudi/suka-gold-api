from rest_framework import serializers
from wallet.models import qris_webhook
from wallet.models import topup_qris_webhook
from datetime import datetime


class PaymentDetailSerializer(serializers.Serializer):
    receipt_id = serializers.CharField()
    source = serializers.CharField()


class QRISPaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = qris_webhook
        fields = "__all__"

    def create(self, validated_data):

        # if topup
        print(validated_data, "validated_data in QRISPaymentWebhookSerializer")

        return qris_webhook.objects.create(**validated_data)

    def to_internal_value(self, data):
        # Flatten nested structure for model compatibility
        data = {
            "event": data.get("event"),
            "created": data.get("created"),
            "business_id": data.get("business_id"),
            "data_id": data["data"].get("id"),
            "data_business_id": data["data"].get("business_id"),
            "currency": data["data"].get("currency"),
            "amount": data["data"].get("amount"),
            "status": data["data"].get("status"),
            "data_created": data["data"].get("created"),
            "qr_id": data["data"].get("qr_id"),
            "qr_string": data["data"].get("qr_string"),
            "reference_id": data["data"].get("reference_id"),
            "type": data["data"].get("type"),
            "channel_code": data["data"].get("channel_code"),
            "expires_at": data["data"].get("expires_at"),
            "branch_code": data["data"]["metadata"].get("branch_code"),
            "receipt_id": data["data"]["payment_detail"].get("receipt_id"),
            "source": data["data"]["payment_detail"].get("source"),
        }
        return super().to_internal_value(data)
