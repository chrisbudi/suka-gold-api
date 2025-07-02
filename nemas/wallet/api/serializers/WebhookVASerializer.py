# serializers.py
from rest_framework import serializers

from wallet.models import virtual_account_webhook


class VirtualAccountPaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = virtual_account_webhook
        fields = "__all__"

    def create(self, validated_data):

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
