# serializers.py
from rest_framework import serializers
from reporting.contracts.gold_transaction import GoldTransactionContract


class GoldTransactionContractSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    transaction_date = serializers.CharField()
    transaction_id = serializers.CharField()
    weight = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=4)
    admin_weight = serializers.DecimalField(
        allow_null=True, max_digits=10, decimal_places=4
    )
    price = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=16)
    admin_price = serializers.DecimalField(
        allow_null=True, decimal_places=2, max_digits=16
    )
    gold_history_price_base = serializers.FloatField(allow_null=True)
    ref_number = serializers.CharField()
    transaction_type = serializers.CharField()
