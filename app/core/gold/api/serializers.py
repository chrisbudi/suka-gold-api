"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import gold, gold_price_config, gold_price, gold_cert_price


# region Gold
class GoldSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold
        fields = [
            "gold_weight",
            "type",
            "brand",
            "certificate_number",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "gold_id",
        ]


class GoldServiceFilter(filters.FilterSet):
    class Meta:
        model = gold

        fields = {
            "type": ["icontains"],
        }


# endregion


# region Price Config
class GoldPriceConfigSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_price_config
        fields = [
            "gpc_code",
            "gpc_description",
            "gold_price_weight",
            "gold_price_setting_model_buy_weekday",
            "gold_price_setting_model_sell_weekday",
            "gold_price_setting_model_buy_weekend",
            "gold_price_setting_model_sell_weekend",
            "gpc_active",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "gpc_id",
        ]


class GoldPriceConfigServiceFilter(filters.FilterSet):
    class Meta:
        model = gold_price_config

        fields = {
            "gpc_code": ["icontains"],
            "gpc_description": ["icontains"],
        }


# endregion


# region Gold Price
class GoldPriceSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_price
        fields = [
            "gold_price_source",
            "gold_price_weight",
            "gold_price_base",
            "gold_price_sell",
            "gold_price_buy",
            "timestamps",
        ]
        read_only_fields = [
            "gold_price_id",
        ]


class GoldPriceServiceFilter(filters.FilterSet):
    class Meta:
        model = gold_price

        fields = {
            "gold_price_source": ["icontains"],
        }


# endregion


# region Cert Price Config
class GoldCertPriceSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_cert_price
        fields = [
            "cert_code",
            "cert_id",
            "gold_weight",
            "cert_price",
        ]
        read_only_fields = [
            "cert_id",
        ]


class GoldCertPriceServiceFilter(filters.FilterSet):
    class Meta:
        model = gold_cert_price

        fields = {
            "cert_code": ["icontains"],
        }


# endregion
