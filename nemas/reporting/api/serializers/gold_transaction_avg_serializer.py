# serializers.py
from rest_framework import serializers
from reporting.contracts.gold_transaction import GoldTransactionContract


class GoldTransactionAvgContractSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    percentage_from_sell = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
    percentage_from_buy = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
    current_gold_price_buy = serializers.DecimalField(
        max_digits=16, decimal_places=2, required=False, allow_null=True
    )
    current_gold_price_sell = serializers.DecimalField(
        max_digits=16, decimal_places=2, required=False, allow_null=True
    )
