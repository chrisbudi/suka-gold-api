from datetime import datetime
import uuid
from rest_framework import serializers
from order.models import order_cart, order_cart_detail
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from core.domain.gold import gold as GoldModel, gold_price

from decimal import Decimal

User = get_user_model()


class GoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldModel
        fields = "__all__"  # Serialize all fields of the gold model


class AddCartDetailSerializer(serializers.ModelSerializer):
    # gold = serializers.PrimaryKeyRelatedField(
    #     queryset=GoldModel.objects.all(), write_only=True
    # )
    gold_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = order_cart_detail
        fields = [
            "gold_id",
            "quantity",
        ]

    def create(self, validated_data):
        goldModel = GoldModel.objects.select_related("certificate").get(
            gold_id=validated_data["gold_id"]
        )
        certificateModel = goldModel.certificate
        goldPriceModel = gold_price().get_active_price()
        order_cart_detail_model = order_cart_detail.objects.filter(
            gold=goldModel, user_id=self.context["request"].user, completed_cart=False
        ).first()
        if goldModel is None:
            raise serializers.ValidationError("Gold not found")
        if goldPriceModel is None:
            raise serializers.ValidationError("Gold price not found")
        # if order cart detail model any then update the endity

        if order_cart_detail_model:
            order_cart_detail_model.price = (
                ((goldPriceModel.gold_price_buy) * goldModel.gold_weight)
                + (goldModel.certificate.cert_price if goldModel.certificate else 0)
                + (goldModel.product_cost or 0)
            )

            order_cart_detail_model.gold_price = goldPriceModel.gold_price_buy
            order_cart_detail_model.product_cost = goldModel.product_cost
            order_cart_detail_model.weight = goldModel.gold_weight
            order_cart_detail_model.cert_price = (
                certificateModel.cert_price if certificateModel else Decimal("0")
            )

            order_cart_detail_model.quantity = validated_data["quantity"]
            order_cart_detail_model.total_price = (
                ((goldPriceModel.gold_price_buy) * goldModel.gold_weight)
                + (goldModel.certificate.cert_price if goldModel.certificate else 0)
                + (goldModel.product_cost or 0)
            ) * validated_data["quantity"]
            order_cart_detail_model.total_price_round = (
                (
                    ((goldPriceModel.gold_price_buy) * goldModel.gold_weight)
                    // 100
                    * 100
                    + 100
                )
                + (goldModel.certificate.cert_price if goldModel.certificate else 0)
                + (goldModel.product_cost or 0)
            ) * validated_data["quantity"]

            order_cart_detail_model.save()
            return order_cart_detail_model

        # else if not any then create it
        validated_data.update(
            {
                "cert": goldModel.certificate,
                "cert_price": (certificateModel.cert_price if certificateModel else 0),
                "product_cost": goldModel.product_cost,
                "gold": goldModel,
                "user": self.context["request"].user,
                "price": goldPriceModel.gold_price_buy,
                "weight": goldModel.gold_weight,
                "total_price": (
                    ((goldPriceModel.gold_price_buy) * goldModel.gold_weight)
                    + (goldModel.certificate.cert_price if goldModel.certificate else 0)
                    + (goldModel.product_cost or 0)
                ),
                "total_price_round": (
                    (
                        ((goldPriceModel.gold_price_buy) * goldModel.gold_weight)
                        // 100
                        * 100
                        + 100
                    )
                    + (goldModel.certificate.cert_price if goldModel.certificate else 0)
                    + (goldModel.product_cost or 0)
                )
                * validated_data["quantity"],
                "completed_cart": False,
            }
        )
        return order_cart_detail.objects.create(**validated_data)


class ProcessCartSerializer(serializers.Serializer):
    # logic for processing the submited cart

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        order_cart_detail_model = order_cart_detail.objects.filter(
            user=validated_data["user"],
            completed_cart=False,
        )
        if not order_cart_detail_model:
            raise serializers.ValidationError("Cart is empty")

        order_cart_instance, created = order_cart.objects.get_or_create(
            user=validated_data["user"],
            completed_cart=False,
            defaults={
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "total_weight": 0,
                "total_price": 0,
                "total_price_round": 0,
            },
        )

        order_cart_instance.total_weight = Decimal(
            sum([item.weight for item in order_cart_detail_model])
        )
        order_cart_instance.total_price = Decimal(
            sum([item.total_price for item in order_cart_detail_model])
        )
        order_cart_instance.total_price_round = Decimal(
            sum([item.total_price_round for item in order_cart_detail_model])
        )
        if created:
            order_cart_instance.created_at = datetime.now()
            order_cart_instance.updated_at = datetime.now()
            order_cart_instance.session_key = str(uuid.uuid4())
            order_cart_instance.save()
        else:
            order_cart_instance.updated_at = datetime.now()
            order_cart_instance.save()

        for item in order_cart_detail_model:
            item.cart = order_cart_instance
            item.save()

        print(CartSerializer(order_cart_instance), "order_cart_instance")
        return CartSerializer(order_cart_instance)


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
            "total_price_round",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "order_cart_detail_id",
            "total_price_round",
            "created_at",
            "updated_at",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):
    order_cart_detail = serializers.SerializerMethodField()

    def get_order_cart_detail(self, obj):
        details = order_cart_detail.objects.filter(cart_id=obj.order_cart_id)
        return CartDetailSerializer(details, many=True).data

    class Meta:
        model = order_cart
        fields = [
            "order_cart_id",
            "total_weight",
            "total_price",
            "total_price_round",
            "created_at",
            "updated_at",
            "completed_cart",
            "session_key",
            "order_cart_detail",
        ]
        depth = 1  # Load related order cart detail with nested serialization
        read_only_fields = [
            "order_cart_id",
            "total_weight",
            "total_price",
            "created_at",
            "updated_at",
            "completed_cart",
            "session_key",
        ]
