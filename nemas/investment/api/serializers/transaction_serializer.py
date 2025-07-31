from core.domain import InvestmentReturn, gold_price
import investment
from investment.models import TransactionModel
from rest_framework import serializers

from django_filters import rest_framework as filters


class InvestmentReturnSerializer(serializers.ModelSerializer):
    """Serializer for investment return model"""

    class Meta:
        model = InvestmentReturn
        fields = [
            "name",
            "rate",
            "duration_days",
            "description",
        ]


class TransactionSerializer(serializers.ModelSerializer):

    investor_name = serializers.CharField(source="investor.name", read_only=True)
    investor_return = InvestmentReturnSerializer(
        source="investment_return", read_only=True
    )

    class Meta:
        model = TransactionModel
        fields = (
            "amount_invested",
            "weight_invested",
            "date_invested",
            "investor_name",
            "investment_return",
            "investor_return",
            "return_weight",
            "return_amount",
            "date_returned",
            "is_returned",
        )
        read_only_fields = (
            "id",
            "created_at",
            "return_weight",
            "return_amount",
            "date_returned",
            "is_returned",
            "investor",
            "updated_at",
        )

    def validate(self, attrs):
        if attrs.get("amount_invested") <= 0:
            raise serializers.ValidationError(
                "Investment amount must be greater than zero."
            )
        if attrs.get("is_returned") and not attrs.get("date_returned"):
            raise serializers.ValidationError(
                "Date returned must be provided if the investment is returned."
            )
        return attrs

    def create(self, validated_data):
        gold_active = gold_price().get_active_price()
        investment_return = validated_data.data.get("investment_return")
        if not gold_active:
            raise serializers.ValidationError("No active gold price found.")

        # calculate investment return based on gold price active

        validated_data["return_weight"] = (
            validated_data["amount_invested"] / investment_return.rate
        )

        validated_data["return_amount"] = (
            validated_data["return_weight"] * gold_active.gold_price_buy
        )
        validated_data["investor"] = self.context["request"].user
        transaction = TransactionModel.objects.create(**validated_data)
        return transaction


class TransactionFilter(filters.FilterSet):
    """
    Filter for transactions based on user and date.
    """

    class Meta:
        model = TransactionModel
        fields = {
            "investor": ["exact"],
            "date_invested": ["exact", "gte", "lte"],
            "is_returned": ["exact"],
            "status": ["exact"],
        }
