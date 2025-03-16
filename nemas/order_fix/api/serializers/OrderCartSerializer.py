from rest_framework import serializers
from order.models import order_cart, order_cart_detail
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from core.domain.gold import gold as GoldModel, gold_price

User = get_user_model()


class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldModel
        fields = "__all__"  # Serialize all fields of the gold model


class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_cart_detail
        fields = [
            "gold",
            "quantity",
        ]

    def create(self, validated_data):
        goldModel = GoldModel.objects.select_related("certificate").get(
            gold_id=validated_data["gold"].id
        )
        if goldModel is None:
            raise serializers.ValidationError("Gold not found")
        goldPriceModel = gold_price().get_active_price()
        if goldPriceModel is None:
            raise serializers.ValidationError("Gold price not found")

        order_cart_detail_model = order_cart_detail.objects.filter(
            gold=goldModel, user_id=self.context["request"].user
        ).first()

        if not order_cart_detail_model:
            validated_data.update(
                {
                    "certificate": goldModel.certificate,
                    "cert_price": (
                        goldModel.certificate.cert_price if goldModel.certificate else 0
                    ),
                    "user_id": self.context["request"].user,
                    "price": goldPriceModel.gold_price_buy,
                    "weight": goldModel.gold_weight,
                    "total_price": validated_data["price"] * validated_data["quantity"],
                }
            )
            return order_cart_detail.objects.create(**validated_data)

        order_cart_detail_model.quantity += validated_data["quantity"]
        order_cart_detail_model.total_price = (
            order_cart_detail_model.price + (order_cart_detail_model.cert_price or 0)
        ) * order_cart_detail_model.quantity

        order_cart_detail_model.save()
        return order_cart_detail_model


class ProcessCartSerializer(serializers.Serializer):
    # logic for processing the submited cart

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user
        order_cart_detail_model = order_cart_detail.objects.filter(
            user_id=validated_data["user_id"]
        )
        if not order_cart_detail_model:
            raise serializers.ValidationError("Cart is empty")
        order_cart_instance = order_cart.objects.create(
            user_id=validated_data["user_id"],
            total_price=sum(
                [
                    (item.total_price + (item.cert_price or 0))
                    for item in order_cart_detail_model
                ]
            ),
            total_weight=sum([item.weight for item in order_cart_detail_model]),
        )
        for item in order_cart_detail_model:
            item.cart_id = order_cart_instance
            item.save()

        return order_cart_instance


class CartDetailSerializer(serializers.ModelSerializer):
    gold = GoldSerializer(read_only=True)

    class Meta:
        model = order_cart_detail
        fields = [
            "order_cart_detail_id",
            "gold",
            "gold_id",
            "cert_price",
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


class CartSerializer(serializers.ModelSerializer):
    order_cart_detail = CartDetailSerializer(many=True, write_only=True)

    class Meta:
        model = order_cart
        fields = [
            "order_cart_id",
            "total_weight",
            "total_price",
            "created_at",
            "updated_at",
            "completed_cart",
            "session_key",
            "order_cart_detail",
        ]
        read_only_fields = [
            "order_cart_id",
            "total_weight",
            "total_price",
            "created_at",
            "updated_at",
            "completed_cart",
            "session_key",
        ]
