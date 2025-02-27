from rest_framework import serializers
from order.models import order_cart, order_cart_detail
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from core.domain.gold import gold as GoldModel

User = get_user_model()


class OrderCartFilter(filters.FilterSet):
    class Meta:
        model = order_cart

        fields = {
            "created_at": ["lte", "gte"],
        }


class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldModel
        fields = "__all__"  # Serialize all fields of the gold model


class OrderCartDetailSerializer(serializers.ModelSerializer):
    gold = serializers.PrimaryKeyRelatedField(
        queryset=GoldModel.objects.all(), write_only=True
    )

    class Meta:
        model = order_cart_detail
        fields = [
            "order_cart_detail_id",
            "gold",
            "weight",
            "price",
            "quantity",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "order_cart_detail_id",
            "created_at",
            "updated_at",
            "total_price",
        ]

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user
        validated_data["total_price"] = (
            validated_data["price"] * validated_data["quantity"]
        )
        return order_cart_detail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.total_price = instance.price * instance.quantity
        return super().update(instance, validated_data)

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
