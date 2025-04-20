from decimal import Decimal
from rest_framework import serializers
from gold_transaction.models import gold_saving_buy
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from user.models import user_props
from core.domain import gold_price

User = get_user_model()


class GoldTransactionBuySerializer(serializers.ModelSerializer):

    class Meta:
        model = gold_saving_buy
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
        # validate if weight and price are equals from gold price
        active_price = gold_price().get_active_price()
        print(
            f"{attrs["weight"]*active_price.gold_price_buy} {attrs["price"]} active price"
        )
        # if (Decimal(attrs["weight"]) * active_price.gold_price_buy) != attrs["price"]:
        #     raise serializers.ValidationError(
        #         "Weight and price are not equals from gold price"
        #     )

        # validate balance is enough
        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_balance(attrs["price"]):
            raise serializers.ValidationError("Balance is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        price = gold_price().get_active_price()
        if price is None:
            raise ValueError("Active gold price not found")

        # Calculate total price before saving

        validated_data["gold_history_price_base"] = price.gold_price_base
        validated_data["gold_history_price_buy"] = price.gold_price_buy

        validated_data["total_price"] = validated_data["price"]

        validated_data["transaction_date"] = datetime.now()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class GoldTransactionBuyFilter(filters.FilterSet):
    class Meta:
        model = gold_saving_buy

        fields = {
            "transaction_date": ["lte", "gte"],
        }
