from datetime import datetime, timedelta
from rest_framework import serializers
from shared_kernel.services.external.xendit_service import va_service, qris_service
from order.models import order_gold, order_gold_detail
from django.contrib.auth import get_user_model
from core.domain.gold import gold as GoldModel
from user.models.users import user_virtual_account as UserVa
from core.domain import bank as core_bank
from uuid import uuid4
import json

User = get_user_model()


class OrderGoldListSerializer(serializers.Serializer):
    order_cart_id = serializers.UUIDField()


class OrderGoldDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_gold_detail
        fields = [
            "order_gold_detail_id",
            "order_gold_id",
            "gold",
            "gold_type",
            "gold_brand",
            "order_weight",
            "order_price",
            "order_qty",
            "order_cert_price",
            "order_detail_total_price",
        ]
        read_only_fields = ["order_gold_detail_id", "order_gold_id"]


class OrderGoldSerializer(serializers.ModelSerializer):
    order_details = OrderGoldDetailSerializer(many=True)

    class Meta:
        model = order_gold
        fields = [
            "order_gold_id",
            "user",
            "order_user_address",
            "order_pickup_customer_datetime",
            "order_pickup_address",
            "order_phone_number",
            "order_item_weight",
            "order_amount",
            "order_payment_va_bank",
            "order_payment_va_number",
            "order_payment_method",
            "order_admin_amount",
            "order_tracking_amount",
            "order_promo_code",
            "order_discount",
            "order_total_price",
            "order_tracking_insurance",
            "order_tracking_packing",
            "order_tracking_insurance_admin",
            "order_tracking_total",
            "order_details",
            "tracking_status_id",
            "tracking_status",
            "tracking_courier",
            "tracking_number",
            "tracking_last_note",
            "tracking_last_updated_datetime",
            "tracking_sla",
        ]
        read_only_fields = [
            "tracking_status_id",
            "tracking_status",
            "tracking_courier",
            "tracking_number",
            "tracking_last_note",
            "tracking_last_updated_datetime",
            "tracking_sla",
            "order_gold_id",
            "order_payment_va_number",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        gold = GoldModel()
        order_details_data = validated_data.pop("order_details")
        validated_data["user"] = self.context["request"].user
        validated_data["order_number"] = gold.generate_number()
        validated_data["order_timestamp"] = datetime.now()

        # if va process payment va
        if validated_data["order_payment_method"] == "VA":
            self.process_va_payment(validated_data, user)
        else:
            validated_data["order_payment_va_bank"] = None
            self.process_qris_payment(validated_data, user)

        validated_data["order_gold_payment_ref"] = self.context["response"][
            "reference_id"
        ]

        order_gold_data = order_gold.objects.create(**validated_data)

        for order_detail_data in order_details_data:

            order_gold_detail.objects.create(
                order_gold=order_gold_data, **order_detail_data
            )

        self.context["response"]["order_gold_id"] = order_gold_data.order_gold_id
        return order_gold

    def process_va_payment(self, validated_data, user):
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

        service = va_service.VAPaymentService()

        payload_json = json.dumps(payload)

        print(payload_json, "payload_json")
        virtual_account = service.va_payment_generate(payload_json)
        if not virtual_account:
            raise serializers.ValidationError("Failed to process VA payment.")

        self.context["response"] = {
            "total_amount": validated_data["order_total_price"],
            "va_number": virtual_account.get("account_number"),
            "reference_id": virtual_account.get("external_id"),
            "order_gold_id": "",
        }

    def process_qris_payment(self, validated_data, user):
        qris = validated_data["order_payment_method"]
        service = qris_service.QRISPaymentService()
        payload = {
            "reference_id": f"qris_generated_user_{user.id}_{str(uuid4())}",
            "type": "DYNAMIC",
            "currency": "IDR",
            "amount": float(validated_data["order_total_price"]),
            "expired_at": (datetime.now() + timedelta(hours=2)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),
            "channel_code": "ID_DANA",
            "is_closed": True,
        }
        payload_json = json.dumps(payload)
        qris = service.qris_payment_generate(payload_json)
        if not qris:
            raise serializers.ValidationError("Failed to process QRIS payment.")
        print(qris, "qris")

        self.context["response"] = {
            "total_amount": validated_data["order_total_price"],
            "qr_string": qris.get("qr_string"),
            "reference_id": qris.get("reference_id"),
            "order_gold_id": "",
        }
