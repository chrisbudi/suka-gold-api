"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.domain import gold, gold_price_config, gold_price, gold_cert_price, gold_promo


# region Gold
class GoldSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold
        fields = [
            "gold_id",
            "gold_weight",
            "type",
            "brand",
            "certificate_number",
            "certificate_weight",
            "gold_image_1",
            "gold_image_2",
            "gold_image_3",
            "gold_image_4",
            "gold_image_5",
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


class GoldUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class GoldImageCodeEnum(serializers.ChoiceField):
        IMAGE1 = "image1"
        IMAGE2 = "image2"
        IMAGE3 = "image3"
        IMAGE4 = "image4"
        IMAGE5 = "image5"

        CHOICES = [
            (IMAGE1, "image1"),
            (IMAGE2, "image2"),
            (IMAGE3, "image3"),
            (IMAGE4, "image4"),
            (IMAGE5, "image5"),
        ]

    gold_image_code = serializers.ChoiceField(choices=GoldImageCodeEnum.CHOICES)

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value


# endregion


# region Price Config
class GoldPriceConfigSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_price_config
        fields = [
            "gpc_id",
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
            "gold_price_id",
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


# region promo
class GoldPromoSerializer(serializers.ModelSerializer):
    """Serializer for gold Promo object"""

    class Meta:
        model = gold_promo
        fields = [
            "gold_promo_id",
            "gold_promo_code",
            "gold_promo_description",
            "gold_promo_weight",
            "gold_promo_amt_pct",
            "gold_promo_amt",
            "gold_promo_min_weight",
            "gold_promo_max_weight",
            "gold_promo_min_amt",
            "gold_promo_max_amt",
            "gold_promo_start_date",
            "gold_promo_end_date",
            "gold_promo_active",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "gold_promo_id",
        ]


class GoldPromoFilter(filters.FilterSet):
    class Meta:
        model = gold_promo

        fields = {
            "gold_promo_code": ["icontains"],
            "gold_promo_description": ["icontains"],
        }


# end region
