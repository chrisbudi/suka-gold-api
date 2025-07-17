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
    gold_id = serializers.IntegerField(write_only=True)
    order_type = serializers.ChoiceField(
        choices=[("buy", "Buy"), ("redeem", "Redeem")], write_only=True
    )
    quantity = serializers.IntegerField(write_only=True, default=1, min_value=1)

    class Meta:
        model = order_cart_detail
        fields = ["gold_id", "quantity", "order_type"]

    def create(self, validated_data):
        goldModel = GoldModel.objects.select_related("certificate").get(
            gold_id=validated_data["gold_id"]
        )
        certificateModel = goldModel.certificate
        goldPriceModel = gold_price().get_active_price()
        order_cart_detail_model = order_cart_detail.objects.filter(
            gold=goldModel,
            user_id=self.context["request"].user,
            completed_cart=False,
            order_type=validated_data["order_type"],
        ).first()
        if goldModel is None:
            raise serializers.ValidationError("Gold not found")
        if goldPriceModel is None:
            raise serializers.ValidationError("Gold price not found")
        # if order cart detail model any then update the endity

        if validated_data["order_type"] == "redeem":
            order_cart().remove_all_uncompleted()
            order_cart_detail().remove_all_uncompleted()

            gold_price_value = goldPriceModel.gold_price_buy * goldModel.gold_weight

            gold_price_value_round = (
                goldPriceModel.gold_price_buy * goldModel.gold_weight // 100 * 100 + 100
            )
            redeem_price = Decimal(goldModel.redeem_price)

            price = Decimal(certificateModel.cert_price if certificateModel else 0) + (
                goldModel.product_cost or 0
            )
            price_round = price
            order_price = gold_price_value + price
            order_price_round = (gold_price_value // 100 * 100 + 100) + price
            total_price = price * validated_data["quantity"] + redeem_price
            total_price_round = (price) * validated_data["quantity"] + redeem_price
        else:

            redeem_price = Decimal(0)
            price = goldPriceModel.gold_price_buy * goldModel.gold_weight
            price_round = price // 100 * 100 + 100
            order_price = (
                price
                + goldModel.product_cost
                + (certificateModel.cert_price if certificateModel else 0)
            )
            order_price_round = (
                price_round
                + goldModel.product_cost
                + (certificateModel.cert_price if certificateModel else 0)
            )

            gold_price_value = order_price
            gold_price_value_round = order_price_round

            total_price = (
                price
                + goldModel.product_cost
                + (certificateModel.cert_price if certificateModel else 0)
            ) * validated_data["quantity"]

            total_price_round = (
                price_round
                + goldModel.product_cost
                + (certificateModel.cert_price if certificateModel else 0)
            ) * validated_data["quantity"]

        if order_cart_detail_model:
            order_cart_detail_model.price = price
            order_cart_detail_model.gold_price = gold_price_value
            order_cart_detail_model.gold_price_round = gold_price_value_round
            order_cart_detail_model.order_price = order_price
            order_cart_detail_model.order_price_round = order_price_round
            order_cart_detail_model.product_cost = goldModel.product_cost
            order_cart_detail_model.weight = goldModel.gold_weight
            order_cart_detail_model.cert_price = Decimal(
                certificateModel.cert_price if certificateModel else 0
            )
            order_cart_detail_model.quantity = validated_data["quantity"]
            order_cart_detail_model.total_price = total_price
            order_cart_detail_model.total_price_round = total_price_round
            order_cart_detail_model.redeem_price = redeem_price
            order_cart_detail_model.order_type = validated_data["order_type"]
            order_cart_detail_model.save()
            return order_cart_detail_model

        validated_data.update(
            {
                "cert": goldModel.certificate,
                "cert_price": (certificateModel.cert_price if certificateModel else 0),
                "product_cost": goldModel.product_cost,
                "gold": goldModel,
                "user": self.context["request"].user,
                "price": price,
                "gold_price": gold_price_value,
                "gold_price_round": gold_price_value_round,
                "order_price": order_price,
                "order_price_round": order_price_round,
                "weight": goldModel.gold_weight,
                "total_price": total_price,
                "total_price_round": total_price_round,
                "completed_cart": False,
                "redeem_price": redeem_price,
                "order_type": validated_data["order_type"],
            }
        )
        return order_cart_detail.objects.create(**validated_data)


class ProcessCartSerializer(serializers.Serializer):
    # logic for processing the submited cart
    order_type = serializers.ChoiceField(
        choices=[("buy", "Buy"), ("redeem", "Redeem")], write_only=True
    )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        order_cart_detail_model = order_cart_detail.objects.filter(
            user=validated_data["user"],
            completed_cart=False,
            order_type=validated_data.get("order_type"),
        )
        if not order_cart_detail_model:
            raise serializers.ValidationError("Cart is empty")

        order_cart_instance, created = order_cart.objects.get_or_create(
            user=validated_data["user"],
            completed_cart=False,
            order_type=validated_data.get("order_type"),
            defaults={
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "total_weight": 0,
                "total_price": 0,
                "total_price_round": 0,
            },
        )

        order_cart_instance.total_weight = Decimal(
            sum([item.weight * item.quantity for item in order_cart_detail_model])
        )

        order_cart_instance.total_price = Decimal(
            sum([item.total_price for item in order_cart_detail_model])
        )

        order_cart_instance.total_price_round = Decimal(
            sum([item.total_price_round for item in order_cart_detail_model])
        )

        order_cart_instance.order_type = validated_data.get("order_type")

        order_cart_instance.total_redeem_price = Decimal(
            sum([item.redeem_price or 0 for item in order_cart_detail_model])
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
    order_type = serializers.ChoiceField(
        choices=[("buy", "Buy"), ("redeem", "Redeem")], write_only=True
    )

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
            "gold_price",
            "gold_price_round",
            "order_price",
            "order_price_round",
            "total_price",
            "total_price_round",
            "created_at",
            "updated_at",
            "order_type",
            "redeem_price",
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
            "order_type",
            "total_redeem_price",
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
