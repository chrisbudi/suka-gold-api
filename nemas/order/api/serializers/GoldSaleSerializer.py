from rest_framework import serializers
from gold_transaction.models import gold_saving_sell
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
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
            "gold_history_price_base",
            "gold_history_price_sell",
            "total_price",
            "transaction_date",
        ]
        read_only_fields = ["total_price", "transaction_date"]

    def validate(self, attrs):
        # validate balance is enough

        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_weight(attrs["weight"]):
            raise serializers.ValidationError("Balance gold is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        # Calculate total price before saving
        validated_data["total_price"] = validated_data["price"]
        # TODO: get data price per gram from price will be updated in the future
        # validated_data["price_per_gram"] = validated_data["price"]
        validated_data["transaction_date"] = datetime.now()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class GoldTransactionSellFilter(filters.FilterSet):
    class Meta:
        model = gold_saving_sell

        fields = {
            "transaction_date": ["lte", "gte"],
        }
