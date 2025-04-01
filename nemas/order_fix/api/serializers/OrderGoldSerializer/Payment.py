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
        if not qris:
            raise serializers.ValidationError("Failed to process QRIS payment.")

        if qris.get("errors") or qris.get("status") == "failed":
            error_message = qris.get("errors", "Failed to process QRIS payment.")
            return serializers.ValidationError(error_message)

        print(qris, "qris")

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
        # self.context["response"] = {
        #     "total_amount": order_amount,
        #     "qr_string": qris.get("qr_string"),
        #     "reference_id": qris.get("reference_id"),
        #     "order_gold_id": order_gold_instance.order_gold_id,
        # }
        return qris
        # return super().create(validated_data)

    def va_payment(self, validated_data, user):
        bank_code = validated_data.get("order_payment_va_bank")
        userVa = UserVa.objects.filter(user=user).first()
        coreBank = core_bank.objects.get(bank_merchant_code=bank_code)
        validated_data["order_payment_va_number"] = (
            f"{str(coreBank.bank_create_code_va)}{userVa.va_number.removeprefix(userVa.merchant_code)}"
            if userVa
            else str(coreBank.bank_create_code_va) + coreBank.generate_va()
        )

        payload = {
            "external_id": f"va_generated_invoice_user_{user.id}_{str(uuid4())}",
            "bank_code": bank_code,
            "name": user.name,
            "expected_amount": float(validated_data["order_total_price"]),
            "expiration_date": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "virtual_account_number": validated_data["order_payment_va_number"],
            "is_closed": True,
            "is_single_use": True,
        }

        service = VAPaymentService()

        payload_json = json.dumps(payload)

        print(payload_json, "payload_json")
        virtual_account = service.va_payment_generate(payload_json)
        if not virtual_account:
            raise serializers.ValidationError("Failed to process VA payment.")

        # self.context["response"] = {
        #     "total_amount": validated_data["order_total_price"],
        #     "va_number": virtual_account.get("account_number"),
        #     "reference_id": virtual_account.get("external_id"),
        #     "order_gold_id": "",
        # }
