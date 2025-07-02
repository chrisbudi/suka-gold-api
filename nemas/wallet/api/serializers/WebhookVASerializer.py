# serializers.py
from rest_framework import serializers

from wallet.models import virtual_account_webhook


class VirtualAccountPaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = virtual_account_webhook
        fields = "__all__"

    def create(self, validated_data):
        external_id = validated_data.get("external_id")
        if not external_id:
            raise serializers.ValidationError("External ID is required.")
        if external_id.startswith("va-topup_"):
            # this is a top-up transaction get topup_transaction
            from wallet.models import topup_transaction

            topup = topup_transaction.objects.filter(
                topup_payment_ref=external_id
            ).first()
            if not topup:
                raise serializers.ValidationError("Top-up transaction not found.")
            # Update the top-up transaction with the webhook data
            topup.topup_status = "PAID"
            topup.save()

        elif external_id.startswith("va-order_"):
            # this is an order transaction get order_gold
            from order.models import order_gold

            order = order_gold.objects.filter(
                order_gold_payment_ref=external_id
            ).first()
            if not order:
                raise serializers.ValidationError("Order transaction not found.")
            # Update the order with the webhook data
            order.order_gold_payment_status = "PAID"
            order.save()
        else:
            # Handle other cases or raise an error
            raise serializers.ValidationError("Invalid external ID format.")

        return super().create(validated_data)

    def to_internal_value(self, data):
        # Map the incoming JSON to the model
        data = {
            "updated": data.get("updated"),
            "created": data.get("created"),
            "payment_id": data.get("payment_id"),
            "callback_virtual_account_id": data.get("callback_virtual_account_id"),
            "owner_id": data.get("owner_id"),
            "external_id": data.get("external_id"),
            "account_number": data.get("account_number"),
            "bank_code": data.get("bank_code"),
            "amount": data.get("amount"),
            "transaction_timestamp": data.get("transaction_timestamp"),
            "merchant_code": data.get("merchant_code"),
            "raw_id": data.get("id"),
        }
        return super().to_internal_value(data)
