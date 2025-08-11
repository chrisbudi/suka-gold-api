from decimal import Decimal
from rest_framework import serializers
from gold_transaction.models import gold_saving_buy
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import date, datetime, timedelta
from common.generator import generate_alphanumeric_code
from user.models import user_props
from core.domain import gold_price
from gold_transaction.repositories.gold_stock_repository import GoldStockRepository

User = get_user_model()


class GoldInOutStockSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=["IN", "OUT"])
    weight = serializers.DecimalField(max_digits=16, decimal_places=4)

    note = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        active_price = gold_price().get_active_price()

        validated_data["price_base"] = active_price.gold_price_base
        validated_data["price_buy"] = active_price.gold_price_buy
        validated_data["price_sell"] = active_price.gold_price_sell

        if validated_data["transaction_type"] == "IN":
            return GoldStockRepository(user).stock_in(
                grams=validated_data["weight"],
                price_base=validated_data.get("price_base"),
                price_buy=validated_data.get("price_buy"),
                note=validated_data.get("note"),
            )
        else:
            return GoldStockRepository(user).stock_out(
                grams=validated_data["weight"],
                price_base=validated_data.get("price_base"),
                price_sell=validated_data.get("price_sell"),
                note=validated_data.get("note"),
            )
