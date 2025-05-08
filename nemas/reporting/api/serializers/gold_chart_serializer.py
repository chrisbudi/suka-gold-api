# serializers.py
from rest_framework import serializers
from reporting.contracts.gold_transaction import GoldTransactionContract


class GoldChartHoursContractSerializer(serializers.Serializer):
    hour = serializers.CharField()
    gold_price_sell = serializers.FloatField()
    gold_price_buy = serializers.FloatField()


class GoldChartDaysContractSerializer(serializers.Serializer):
    day = serializers.CharField()
    gold_price_buy = serializers.FloatField()
    gold_price_sell = float
    timestamps = serializers.CharField()
