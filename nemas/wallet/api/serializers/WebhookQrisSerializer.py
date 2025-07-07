from rest_framework import serializers
from wallet.models import qris_webhook
from datetime import datetime

from wallet.models.topup import topup_transaction


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
        reference_id = validated_data.get("reference_id")
        if not reference_id:
            raise serializers.ValidationError("Reference ID is required.")
        if reference_id.startswith("qris-topup_"):
            # this is a top-up transaction get topup_qris_webhook
            topup = topup_transaction.objects.filter(reference_id=reference_id).first()
            if not topup:
                raise serializers.ValidationError("Top-up transaction not found.")
            # Update the top-up transaction with the webhook data
            topup.update_status("PAID")
            topup.save()

        elif reference_id.startswith("qris-order_"):
            # this is an order transaction get order_gold
            from order.models import order_gold

            order = order_gold.objects.filter(
                order_gold_payment_ref=reference_id
            ).first()
            if not order:
                raise serializers.ValidationError("Order transaction not found.")
            # Update the order with the webhook data
            order.update_payment_status("PAID")
            order.save()
        else:
            # Handle other cases or raise an error
            raise serializers.ValidationError("Invalid reference ID format.")

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
            # "receipt_id": data["data"]["payment_detail"].get("receipt_id"),
            # "source": data["data"]["payment_detail"].get("source"),
        }
        return super().to_internal_value(data)
