from datetime import datetime, timedelta
from decimal import Decimal
from rest_framework import serializers
from order_fix.api.serializers.OrderGoldSerializer.Payment import PaymentProcess
from shared_kernel.services.external.sapx_service import SapxService
from order.models.order_cart import order_cart_detail
from order.models import order_cart, order_payment
from shared_kernel.services.external.xendit_service import va_service, qris_service
from order.models import order_gold, order_gold_detail
from django.contrib.auth import get_user_model
from core.domain.gold import gold as GoldModel
from user.models.users import user_virtual_account as UserVa, user_address
from core.domain import bank as core_bank
from uuid import UUID, uuid4
import json
from django.db import transaction

User = get_user_model()


class SubmitOrderGoldSerializer(serializers.ModelSerializer):
    order_cart_id = serializers.UUIDField()
    order_user_address_id = serializers.IntegerField()
    order_payment_method_id = serializers.IntegerField()
    order_payment_method_name = serializers.CharField()
    order_payment_va_bank = serializers.CharField(allow_null=True, required=False)
    tracking_courier_service_id = serializers.IntegerField()
    tracking_courier_service_code = serializers.CharField()
    tracking_courier_id = serializers.IntegerField()

    class Meta:
        model = order_gold
        # cart --> item
        # courier --> delivery
        # payment_method --> payment
        # user_address --> address
        # promo --> promo
        fields = [
            "order_cart_id",
            "order_user_address_id",
            "order_payment_method_id",
            "order_payment_method_name",
            "order_payment_va_bank",
            "tracking_courier_service_id",
            "tracking_courier_service_code",
            "tracking_courier_id",
        ]

    def validate(self, data):
        # if payment qris then max payment in 10.000.000
        if data.get("order_payment_method_name") == "QRIS":
            order_cart_id = data.get("order_cart_id")
            order_cart_models = order_cart.objects.get(order_cart_id=order_cart_id)
            if order_cart_models.total_price > 10000000:
                raise serializers.ValidationError("Payment QRIS max 10.000.000")

    def create(self, validated_data):
        user = self.context["request"].user
        user_address_id = validated_data.get("order_user_address_id")
        user_address_model = user_address.objects.filter(id=user_address_id).first()

        userVa = UserVa.objects.filter(user=user).first()
        coreBank = core_bank.objects.get(
            bank_merchant_code=validated_data.get("order_payment_va_bank")
        )
        virtual_account_number = (
            f"{coreBank.bank_create_code_va}{userVa.va_number[len(userVa.merchant_code):]}"
            if userVa
            else f"{coreBank.bank_create_code_va}{coreBank.generate_va()}"
        )
        order_cart_id = validated_data.get("order_cart_id")

        order_cart_models = order_cart.objects.get(order_cart_id=order_cart_id)

        print(order_cart_models, "order_cart_models")
        order_cart_details_model = (
            order_cart_detail.objects.select_related("cert")
            .select_related("gold")
            .filter(cart_id=order_cart_id)
        )

        if user_address_model is None:
            raise serializers.ValidationError("User address not found")

        if not order_cart_models and not order_cart_details_model:
            raise serializers.ValidationError("Order cart not found")

        shipping_weight = order_cart_models.total_weight
        order_amount = order_cart_models.total_price

        # shipping region
        sapx_service = SapxService()
        payload = sapx_service.generate_payload(
            order_amount,
            shipping_weight,
            "",
            "",
        )
        payload_data = json.dumps(payload)

        shipping_data = sapx_service.get_price(payload_data)
        if shipping_data.get("status") == "failed":
            self.context["response"] = {"message": shipping_data.get("message")}
            return serializers.ValidationError(shipping_data.get("message"))
        print(shipping_data, "shipping_data")
        tracking_service_code = validated_data.get("tracking_courier_service_code")
        # mapping shipping data
        services = list(
            filter(
                lambda s: s.get("service_type_code") == tracking_service_code,
                shipping_data.get("data", {}).get("services", []),
            )
        )
        service = next(iter(services), {})
        insurance = service.get("insurance")
        insurance_admin = service.get("insurance_admin")
        packing = service.get("packing")
        cost = service.get("cost")
        shipping_total = Decimal(service.get("total") or 0)
        shipping_total_rounded = shipping_total // 100 * 100 + 100

        # Insert data from order_cart into order_gold

        with transaction.atomic():
            validated_data.update(
                {
                    "order_timestamp": datetime.now(),
                    "order_user_address": user_address_model,
                    "user": user,
                    "order_payment_method_id": validated_data.get(
                        "order_payment_method_id"
                    ),
                    "order_payment_method_name": validated_data.get(
                        "order_payment_method_name"
                    ),
                    "order_phone_number": user.phone_number,
                    "order_item_weight": order_cart_models.total_weight,
                    "order_amount": order_amount,
                    "order_admin_amount": 0,
                    "order_pickup_address": None,
                    "order_pickup_customer_datetime": None,
                    "order_tracking_amount": cost,
                    "order_tracking_insurance": insurance,
                    "order_tracking_packing": packing,
                    "order_tracking_insurance_admin": insurance_admin,
                    "order_tracking_total_amount": shipping_total,
                    "order_tracking_total_amount_rounded": shipping_total_rounded,
                    "order_promo_code": None,
                    "order_discount": 0,
                    "order_total_price": (
                        order_cart_models.total_price + shipping_total_rounded
                    ),
                    "tracking_courier_id": validated_data.get("tracking_courier_id"),
                    "tracking_courier_service_id": validated_data.get(
                        "tracking_courier_service_id"
                    ),
                    "tracking_status_id": "0",
                    "order_status": "PENDING",
                }
            )
            order_gold_instance = order_gold.objects.create(**validated_data)

            # create order_gold
            for cart_detail in order_cart_details_model:
                detailGold = GoldModel.objects.get(gold_id=cart_detail.gold.gold_id)
                order_gold_detail.objects.create(
                    order_gold=order_gold_instance,
                    gold=detailGold,
                    gold_type=detailGold.type,
                    gold_brand=detailGold.brand,
                    weight=detailGold.gold_weight,
                    order_price=cart_detail.price,
                    qty=cart_detail.quantity,
                    cert=cart_detail.cert,
                    cert_price=cart_detail.cert_price,
                    product_cost=cart_detail.product_cost,
                    order_detail_total_price=cart_detail.total_price,
                )

            # process payment
            process = PaymentProcess(order_gold_instance)

            # if qris
            if validated_data.get("order_payment_method_name") == "QRIS":
                pay_ref = process.qris_payment(
                    validated_data, order_amount, user, order_gold_instance
                )
            else:
                pay_ref = process.va_payment(validated_data, user)

            if isinstance(pay_ref, dict) and (
                pay_ref.get("errors") or pay_ref.get("status") == "failed"
            ):
                error_message = pay_ref.get("errors") or "Failed to process payment."
                raise serializers.ValidationError({"payment_error": error_message})

        return order_gold_instance

    # def process_va_payment_method(
    #     self, validated_data, order_amount, user, order_gold_instance
    # ):
    #     payment_service = VAPaymentService()

    #     payload = payment_service.generate_payload(
    #         float(order_amount),
    #         f"qris_generated_user_{user.id}_{str(uuid4())}",
    #         validated_data.get("order_payment_va_bank"),
    #         user,
    #         validated_data.get("order_payment_va_number"),
    #     )
    #     payload_json = json.dumps(payload)

    #     vaPaymentMethod = payment_service.va_payment_generate(payload_json)
    #     if not vaPaymentMethod:
    #         raise serializers.ValidationError(
    #             "Failed to process vaPaymentMethod payment."
    #         )

    #     if vaPaymentMethod.get("errors") or vaPaymentMethod.get("status") == "failed":
    #         error_message = vaPaymentMethod.get(
    #             "errors", "Failed to process vaPaymentMethod payment."
    #         )
    #         self.context["response"] = {"message": error_message}
    #         return serializers.ValidationError(error_message)

    #     print(vaPaymentMethod, "vaPaymentMethod")

    #     # generate payment payload
    #     order_payment.objects.create(
    #         order_payment_ref=vaPaymentMethod.get("reference_id"),
    #         order_payment_status="PENDING",
    #         order_payment_method_id=validated_data.get("order_payment_method_id"),
    #         order_payment_va_bank=validated_data.get("order_payment_va_bank"),
    #         order_payment_va_number=validated_data.get("order_payment_va_number"),
    #         order_payment_amount=order_amount,
    #         order_payment_admin_amount=0,
    #         order_payment_number=vaPaymentMethod.get("qr_string"),
    #         order_payment_method_name=validated_data.get("order_payment_method_name"),
    #         order_gold=order_gold_instance,
    #         order_payment_timestamp=datetime.now(),
    #     )

    #     self.context["response"] = {
    #         "total_amount": order_amount,
    #         "qr_string": vaPaymentMethod.get("qr_string"),
    #         "reference_id": vaPaymentMethod.get("reference_id"),
    #         "order_gold_id": order_gold_instance.order_gold_id,
    #     }
    #     return vaPaymentMethod

    # def process_qris_payment_method(
    #     self, validated_data, order_amount, user, order_gold_instance
    # ):
    #     payment_service = QRISPaymentService()

    #     payload = payment_service.generate_payload(
    #         float(order_amount),
    #         f"qris_generated_user_{user.id}_{str(uuid4())}",
    #     )
    #     payload_json = json.dumps(payload)

    #     qris = payment_service.qris_payment_generate(payload_json)
    #     if not qris:
    #         raise serializers.ValidationError("Failed to process QRIS payment.")

    #     if qris.get("errors") or qris.get("status") == "failed":
    #         error_message = qris.get("errors", "Failed to process QRIS payment.")
    #         self.context["response"] = {"message": error_message}
    #         return serializers.ValidationError(error_message)

    #     print(qris, "qris")

    #     # generate payment payload
    #     order_payment.objects.create(
    #         order_payment_ref=qris.get("reference_id"),
    #         order_payment_status="PENDING",
    #         order_payment_method_id=validated_data.get("order_payment_method_id"),
    #         order_payment_va_bank=validated_data.get("order_payment_va_bank"),
    #         order_payment_va_number=validated_data.get("order_payment_va_number"),
    #         order_payment_amount=order_amount,
    #         order_payment_admin_amount=0,
    #         order_payment_number=qris.get("qr_string"),
    #         order_payment_method_name=validated_data.get("order_payment_method_name"),
    #         order_gold=order_gold_instance,
    #         order_payment_timestamp=datetime.now(),
    #     )
    #     self.context["response"] = {
    #         "total_amount": order_amount,
    #         "qr_string": qris.get("qr_string"),
    #         "reference_id": qris.get("reference_id"),
    #         "order_gold_id": order_gold_instance.order_gold_id,
    #     }
    #     return qris
    # return super().create(validated_data)


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
            "weight",
            "order_price",
            "qty",
            "cert_price",
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
            "order_tracking_total_amount",
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


#     def create(self, validated_data):
#         user = self.context["request"].user
#         gold = GoldModel()
#         order_details_data = validated_data.pop("order_details")
#         validated_data["user"] = self.context["request"].user
#         validated_data["order_number"] = gold.generate_number()
#         validated_data["order_timestamp"] = datetime.now()

#         # # if va process payment va
#         # if validated_data["order_payment_method"] == "VA":
#         #     self.process_va_payment(validated_data, user)
#         # else:
#         #     validated_data["order_payment_va_bank"] = None
#         #     self.process_qris_payment(validated_data, user)

#         validated_data["order_gold_payment_ref"] = self.context["response"][
#             "reference_id"
#         ]

#         order_gold_data = order_gold.objects.create(**validated_data)

#         for order_detail_data in order_details_data:

#             order_gold_detail.objects.create(
#                 order_gold=order_gold_data, **order_detail_data
#             )

#         self.context["response"]["order_gold_id"] = order_gold_data.order_gold_id
#         return order_gold

# def process_va_payment(self, validated_data, user):

# def process_qris_payment(self, validated_data, user):
#     qris = validated_data["order_payment_method"]
#     service = qris_service.QRISPaymentService()
#     payload = {
#         "reference_id": f"qris_generated_user_{user.id}_{str(uuid4())}",
#         "type": "DYNAMIC",
#         "currency": "IDR",
#         "amount": float(validated_data["order_total_price"]),
#         "expired_at": (datetime.now() + timedelta(hours=2)).strftime(
#             "%Y-%m-%dT%H:%M:%S"
#         ),
#         "channel_code": "ID_DANA",
#         "is_closed": True,
#     }
#     payload_json = json.dumps(payload)
#     qris = service.qris_payment_generate(payload_json)
#     if not qris:
#         raise serializers.ValidationError("Failed to process QRIS payment.")
#     print(qris, "qris")

#     self.context["response"] = {
#         "total_amount": validated_data["order_total_price"],
#         "qr_string": qris.get("qr_string"),
#         "reference_id": qris.get("reference_id"),
#         "order_gold_id": "",
#     }
