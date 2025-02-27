from datetime import datetime
from rest_framework import serializers
from order.models import order_gold, order_gold_detail
from django.contrib.auth import get_user_model
from core.domain.gold import gold as GoldModel

User = get_user_model()


class OrderGoldDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_gold_detail
        fields = [
            "order_gold_detail_id",
            "order_gold_id",
            "gold",
            "gold_type",
            "gold_brand",
            "certificate_number",
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
            "order_phone_number",
            "order_item_weight",
            "order_amount",
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
        ]

    def create(self, validated_data):
        gold = GoldModel()
        order_details_data = validated_data.pop("order_details")
        validated_data["user"] = self.context["request"].user
        validated_data["order_number"] = gold.generate_number()
        validated_data["order_timestamp"] = datetime.now()

        order_gold_data = order_gold.objects.create(**validated_data)

        for order_detail_data in order_details_data:
            order_gold_detail.objects.create(
                order_gold=order_gold_data, **order_detail_data
            )

        return order_gold
