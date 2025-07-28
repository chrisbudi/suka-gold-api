from investment.models import TransactionModel
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = (
            "amount_invested",
            "weight_invested",
            "date_invested",
            "investment_return",
            "investment_weight_return",
            "date_returned",
            "is_returned",
        )
        read_only_fields = ("id", "created_at", "updated_at")

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

        transaction = TransactionModel.objects.create(**validated_data)
        return transaction
