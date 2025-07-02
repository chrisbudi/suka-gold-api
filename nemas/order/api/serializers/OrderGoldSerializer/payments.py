import decimal
from common.responses import NemasReponses
from order.models import order_payment, order_gold
from user.models import user_virtual_account as UserVa
from core.domain import bank as core_bank
from datetime import datetime, timedelta
from shared.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from uuid import uuid4
from decimal import Decimal
from rest_framework import serializers

import json


class PaymentProcess:
    def __init__(self, order):
        self.order = order

    def qris_payment(
        self, validated_data, order_amount, user, order_gold_instance: order_gold
    ):
        payment_service = QRISPaymentService()
        order_amount_summary = order_amount + (order_amount * Decimal(0.7 / 100))
        order_amount_summary_round = order_amount_summary // 100 * 100 + 100
        payload = payment_service.generate_payload(
            float(order_amount_summary_round),
            f"qris-order_{user.id}_{str(uuid4())}",
        )
        payload_json = json.dumps(payload)
        qris = payment_service.qris_payment_generate(payload_json)
        if not qris.get("success"):
            raise serializers.ValidationError(qris)
        # payment_amount = qris["data"].get("amount")
        # generate payment payload
        order_payment.objects.create(
            order_payment_ref=qris["data"].get("reference_id"),
            order_payment_status="ISSUED",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=validated_data.get("order_payment_va_bank"),
            order_payment_amount=order_amount_summary,
            order_payment_summary_amount=order_amount_summary,
            order_payment_summary_amount_round=order_amount_summary_round,
            order_payment_admin_amount=order_amount * Decimal(0.7 / 100),
            order_payment_number=qris["data"].get("qr_string"),
            order_payment_method_name=validated_data.get("order_payment_method_name"),
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )

        # update order gold instance order gold payment ref
        order_gold_instance.order_gold_payment_ref = qris["data"].get("reference_id")
        order_gold_instance.order_gold_payment_status = "ISSUED"
        order_gold_instance.save()

        return NemasReponses.success(
            data={
                "total_amount": order_amount_summary_round,
                "qr_string": qris["data"].get("qr_string"),
                "reference_id": qris["data"].get("reference_id"),
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="QRIS payment generated successfully",
        )

    def va_payment(
        self,
        validated_data,
        order_amount,
        user,
        va_number,
        order_gold_instance: order_gold,
    ):
        payment_service = VAPaymentService()

        order_amount_summary = order_amount + 4500
        order_amount_summary_round = order_amount_summary

        payload = payment_service.generate_payload(
            float(order_amount_summary_round),
            f"va-order_{user.id}_{str(uuid4())}",
            validated_data.get("order_payment_va_bank"),
            user,
            va_number,
        )
        payload_json = json.dumps(payload)

        va_method = payment_service.va_payment_generate(payload_json)

        if not va_method.get("success"):
            raise serializers.ValidationError(va_method)

        print(va_method, "va_method")

        # generate payment payload
        order_pay = order_payment.objects.create(
            order_payment_ref=va_method["data"].get("external_id"),
            order_payment_status="ISSUED",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=validated_data.get("order_payment_va_bank"),
            order_payment_va_number=va_method["data"].get("account_number"),
            order_payment_amount=Decimal(va_method["data"].get("expected_amount")),
            order_payment_summary_amount=order_amount_summary,
            order_payment_summary_amount_round=order_amount_summary_round,
            order_payment_admin_amount=4500,
            order_payment_number=va_method["data"].get("account_number"),
            order_payment_method_name=validated_data.get("order_payment_method_name"),
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )

        # update order gold instance order gold payment ref
        order_gold_instance.order_gold_payment_ref = va_method["data"].get(
            "external_id"
        )
        order_gold_instance.order_gold_payment_status = "ISSUED"
        order_gold_instance.save()

        return NemasReponses.success(
            data={
                "total_amount": order_pay.order_payment_amount,
                "virtual_account": va_method["data"].get("account_number"),
                "reference_id": va_method["data"].get("external_id"),
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="VA payment generated successfully",
        )

    def cash_payment(
        self,
        validated_data,
        order_amount,
        user,
        order_gold_instance: order_gold,
    ):
        payment_service = VAPaymentService()

        order_amount_summary = order_amount
        order_amount_summary_round = order_amount_summary

        # generate payment payload
        order_pay = order_payment.objects.create(
            order_payment_ref="CASH",
            order_payment_status="PAID",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=None,
            order_payment_va_number=None,
            order_payment_amount=order_amount_summary,
            order_payment_summary_amount=order_amount_summary,
            order_payment_summary_amount_round=order_amount_summary_round,
            order_payment_admin_amount=0,
            order_payment_number="Cash",
            order_payment_method_name=validated_data.get("order_payment_method_name"),
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )

        # update order gold instance order gold payment ref
        order_gold_instance.order_gold_payment_ref = "CASH"
        order_gold_instance.order_gold_payment_status = "PAID"
        order_gold_instance.save()

        return NemasReponses.success(
            data={
                "total_amount": order_pay.order_payment_amount,
                "payment_type": "CASH",
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="Cash payment is successfully",
        )

    def redeem_payment(
        self,
        validated_data,
        order_amount,
        user,
        order_gold_instance: order_gold,
    ):

        order_amount_summary = order_amount
        order_amount_summary_round = order_amount_summary

        # generate payment payload
        order_pay = order_payment.objects.create(
            order_payment_ref="GOLD",
            order_payment_status="PAID",
            order_payment_method_id=validated_data.get("order_payment_method_id"),
            order_payment_va_bank=None,
            order_payment_va_number="",
            order_payment_amount=order_amount_summary,
            order_payment_summary_amount=order_amount_summary,
            order_payment_summary_amount_round=order_amount_summary_round,
            order_payment_admin_amount=0,
            order_payment_number="GOLD",
            order_payment_method_name=None,
            order_gold=order_gold_instance,
            order_payment_timestamp=datetime.now(),
        )

        # update order gold instance order gold payment ref
        order_gold_instance.order_gold_payment_ref = "GOLD"
        order_gold_instance.order_gold_payment_status = "PAID"
        order_gold_instance.save()

        return NemasReponses.success(
            data={
                "total_amount": order_pay.order_payment_amount,
                "payment_type": "GOLD",
                "order_gold_id": order_gold_instance.order_gold_id,
            },
            message="VA payment generated successfully",
        )
