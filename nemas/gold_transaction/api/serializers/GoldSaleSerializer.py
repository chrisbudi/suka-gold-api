from decimal import Decimal
from rest_framework import serializers
from gold_transaction.models import gold_saving_sell
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import date, datetime, timedelta
from core.domain import gold_price
from common.generator import generate_alphanumeric_code
from user.models import user_props

User = get_user_model()


class GoldTransactionSellSerializer(serializers.ModelSerializer):

    class Meta:
        model = gold_saving_sell
        fields = [
            "gold_transaction_id",
            "weight",
            "price",
            # TODO: get data price per gram from price will be updated in the future
            "total_price",
            "transaction_date",
        ]
        read_only_fields = ["total_price", "transaction_date"]

    def validate(self, attrs):
        active_price = gold_price().get_active_price()
        # if (Decimal(attrs["weight"]) * active_price.gold_price_sell) == attrs["price"]:
        #     raise serializers.ValidationError(
        #         "Weight and price are not equals from gold price"
        #     )

        # validate balance is enough

        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_weight(attrs["weight"]):
            raise serializers.ValidationError("Balance gold is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        # get active price
        price = gold_price().get_active_price()
        if price is None:
            raise ValueError("Active gold price not found")

        # generate number for transaction
        gold_sell_number = (
            "JE" + date.today().strftime("%y%m") + generate_alphanumeric_code()
        )
        validated_data["gold_sell_number"] = (
            gold_sell_number
            if self.instance is None
            else self.instance.gold_sell_number
        )
        # Calculate total price before saving
        validated_data["gold_history_price_base"] = price.gold_price_base
        validated_data["gold_history_price_sell"] = price.gold_price_sell
        validated_data["total_price"] = validated_data["price"]
        validated_data["transaction_date"] = datetime.now()
        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)


class GoldTransactionSellFilter(filters.FilterSet):
    class Meta:
        model = gold_saving_sell

        fields = {
            "transaction_date": ["lte", "gte"],
        }
