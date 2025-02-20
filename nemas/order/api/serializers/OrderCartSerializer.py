from rest_framework import serializers
from order.models import order_cart, order_cart_detail
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from user.models import user_props
from core.domain.gold import gold as GoldModel

User = get_user_model()


class OrderCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_cart
        fields = [
            "user_id",
            "cart_status",
            "total_weight",
            "total_price",
        ]
        read_only_fields = ["order_cart_id"]

    def validate(self, attrs):
        # validate balance is enough

        # if not user_props.objects.get(
        #     user=self.context["request"].user
        # ).validate_balance(attrs["price"]):
        #     raise serializers.ValidationError("Balance is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        return super().create(validated_data)


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


class AddToCartSerializer(serializers.ModelSerializer):
    gold = GoldSerializer(read_only=True)  # Nest gold details inside cart response
    gold_id = serializers.PrimaryKeyRelatedField(
        queryset=GoldModel.objects.all(), write_only=True
    )

    # gold = goldSerializer  # Include goldSerializer in the fields

    class Meta:
        model = order_cart_detail
        fields = [
            "order_cart_detail_id",
            "gold_id",
            "gold",
            "weight",
            "price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order_cart_detail_id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user

        return order_cart_detail.objects.create(**validated_data)
