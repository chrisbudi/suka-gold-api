from pyexpat import model
from rest_framework import serializers
from django.db import models
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_id = models.CharField(max_length=255)


class SimulatedPaymentQrisSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    class Meta:
        model = Payment
        fields = ["amount", "reference_id"]

    def validate(self, data):
        amount = data.get("amount")
        reference_id = data.get("reference_id")
        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        if not reference_id:
            raise serializers.ValidationError("Reference ID is need")

        return data

    def simulated_payment(self, validated_data):
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]

        try:
            qris_service = QRISPaymentService()
            payload = {
                "amount": amount,
            }
            response = qris_service.qris_payment_simulate(reference_id, payload)
            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))


class SimulatedPaymentVaSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reference_id = serializers.CharField(max_length=255)

    class Meta:
        model = Payment
        fields = ["amount", "reference_id"]

    def validate(self, data):
        amount = data.get("amount")

        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        return data

    def simulated_payment(self, validated_data):
        amount = validated_data["amount"]
        reference_id = validated_data["reference_id"]

        try:
            va_service = VAPaymentService()
            payload = {
                "amount": amount,
            }
            response = va_service.va_payment_simulate(reference_id, payload)
            return response
        except Exception as e:
            raise serializers.ValidationError(str(e))
