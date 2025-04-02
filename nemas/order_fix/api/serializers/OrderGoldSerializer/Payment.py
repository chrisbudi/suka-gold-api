from common.responses import NemasReponses
from order.models import order_payment
from user.models import user_virtual_account as UserVa
from core.domain import bank as core_bank
from datetime import datetime, timedelta
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from uuid import uuid4
from rest_framework import serializers

import json


class PaymentProcess:
    def __init__(self, order):
        self.order = order

    def qris_payment(self, validated_data, order_amount, user, order_gold_instance):
        payment_service = QRISPaymentService()

        payload = payment_service.generate_payload(
            float(order_amount),
            f"qris_generated_user_{user.id}_{str(uuid4())}",
        )
        payload_json = json.dumps(payload)

        qris = payment_service.qris_payment_generate(payload_json)

        if not qris.get("success"):
            raise serializers.ValidationError(qris)

        # generate payment payload
        order_payment.objects.create(
            order_payment_ref=qris.get("reference_id"),
            order_payment_status="PENDING",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=validated_data.get("order_payment_va_bank"),
            order_payment_va_number=validated_data.get("order_payment_va_number"),
            order_payment_amount=order_amount,
            order_payment_admin_amount=0,
            order_payment_number=qris.get("qr_string"),
            order_payment_method_name=validated_data.get("order_payment_method_name"),
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )
        return NemasReponses.success(
            data={
                "total_amount": order_amount,
                "qr_string": qris.get("qr_string"),
                "reference_id": qris.get("reference_id"),
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="QRIS payment generated successfully",
        )

    def va_payment(self, validated_data, order_amount, user, order_gold_instance):
        payment_service = VAPaymentService()

        payload = payment_service.generate_payload(
            float(order_amount),
            f"qris_generated_user_{user.id}_{str(uuid4())}",
            validated_data.get("order_payment_va_bank"),
            user,
            validated_data.get("order_payment_va_number"),
        )
        payload_json = json.dumps(payload)

        va_method = payment_service.va_payment_generate(payload_json)

        if not va_method.get("success"):
            raise serializers.ValidationError(va_method)

        # generate payment payload
        order_payment.objects.create(
            order_payment_ref=va_method.get("reference_id"),
            order_payment_status="PENDING",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=validated_data.get("order_payment_va_bank"),
            order_payment_va_number=validated_data.get("order_payment_va_number"),
            order_payment_amount=order_amount,
            order_payment_admin_amount=0,
            order_payment_number=va_method.get("qr_string"),
            order_payment_method_name=validated_data.get("order_payment_method_name"),
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )

        return NemasReponses.success(
            data={
                "total_amount": order_amount,
                "qr_string": va_method.get("qr_string"),
                "reference_id": va_method.get("reference_id"),
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="VA payment generated successfully",
        )
