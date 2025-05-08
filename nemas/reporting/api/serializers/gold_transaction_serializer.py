# serializers.py
from rest_framework import serializers
from reporting.contracts.gold_transaction import GoldTransactionContract


class GoldTransactionContractSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    transaction_date = serializers.CharField()
    transaction_id = serializers.IntegerField()
    weight = serializers.FloatField(allow_null=True)
    price = serializers.FloatField(allow_null=True)
    gold_history_price_base = serializers.FloatField(allow_null=True)
    ref_number = serializers.CharField()
