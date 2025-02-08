import json
from pyexpat import model
from rest_framework import serializers
from django.db import models
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from wallet.models import topup_transaction


class SimulatedPaymentQrisSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    def validate(self, data):
        amount = data.get("amount")
        reference_id = data.get("reference_id")
        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        print(reference_id, "reference_id")
        if not reference_id:
            raise serializers.ValidationError("Reference ID is need")

        return data

    def create(self, validated_data):
        print(validated_data, "validated_data")
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]
        try:
            qris_service = QRISPaymentService()
            payload = {
                "amount": float(amount),
            }
            payload_json = json.dumps(payload)
            response = qris_service.qris_payment_simulate(reference_id, payload_json)
            print(response, "response")
            topupTransaction = topup_transaction.objects.get(
                topup_payment_ref=reference_id
            )
            topupTransaction.update_status(topup_status="SUCCESS")
            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))


class SimulatedPaymentVaSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    def validate(self, data):
        amount = data.get("amount")

        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        return data

    def create(self, validated_data):
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]
        try:
            va_service = VAPaymentService()
            payload = {
                "amount": float(amount),
            }
            payload_json = json.dumps(payload)
            response = va_service.va_payment_simulate(reference_id, payload_json)

            topupTransaction = topup_transaction.objects.get(
                topup_payment_ref=reference_id
            )
            topupTransaction.update_status(topup_status="SUCCESS")

            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))
