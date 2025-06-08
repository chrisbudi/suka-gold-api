# serializers.py
from rest_framework import serializers
from reporting.contracts.gold_transaction import GoldTransactionContract


class GoldTransactionAvgContractSerializer(serializers.Serializer):
    avg_pct = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
