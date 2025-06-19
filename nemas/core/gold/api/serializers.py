"""
Serializer for recipe api
"""

from datetime import datetime
from os import read
import uuid
from humanize import activate
from rest_framework import serializers
from django_filters import rest_framework as filters
from core.domain import (
    gold,
    gold_price_config,
    gold_price,
    gold_promo,
    gold_cert_detail_price,
    cert,
)
from order.models.order_gold import order_gold_detail


# region cert
class CertSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = cert
        fields = [
            "cert_id",
            "cert_brand",
            "cert_code",
            "gold_weight",
            "cert_price",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "cert_id",
        ]

    def create(self, validated_data):

        certModel = cert.objects.create(
            **validated_data,
            create_user=self.context["request"].user.id,
            create_time=datetime.now(),
            create_user_email=self.context["request"].user.email,
            upd_user=self.context["request"].user.id,
            upd_time=datetime.now(),
            upd_user_email=self.context["request"].user.email,
        )
        return certModel

    def update(self, instance: cert, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.upd_user = self.context["request"].user.id
        instance.upd_time = datetime.now()
        instance.upd_user_email = self.context["request"].user.email
        instance.save()

        return instance


class CertFilterSerializer(filters.FilterSet):
    class Meta:
        model = cert

        fields = {
            "cert_brand": ["icontains"],
            "cert_code": ["icontains"],
        }


# endregion


# region Gold
class GoldSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    certificate = CertSerializer(read_only=True)
    certificate_id = serializers.PrimaryKeyRelatedField(
        queryset=cert.objects.all(), source="certificate", write_only=True
    )

    class Meta:
        model = gold
        fields = [
            "gold_id",
            "gold_weight",
            "type",
            "brand",
            "certificate",
            "certificate_id",
            "certificate_weight",
            "product_cost",
            "gold_image_1",
            "gold_image_2",
            "gold_image_3",
            "gold_image_4",
            "gold_image_5",
        ]
        read_only_fields = [
            "gold_id",
        ]

    def create(self, validated_data):

        goldModel = gold.objects.create(
            **validated_data,
            create_user=self.context["request"].user.id,
            create_time=datetime.now(),
            create_user_email=self.context["request"].user.email,
            upd_user=self.context["request"].user.id,
            upd_time=datetime.now(),
            upd_user_email=self.context["request"].user.email,
        )

        return goldModel

    def update(self, instance: gold, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.upd_user = self.context["request"].user.id
        instance.upd_time = datetime.now()
        instance.upd_user_email = self.context["request"].user.email
        instance.save()

        return instance


class GoldProductShowSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    certificate = CertSerializer(read_only=True)
    certificate_id = serializers.PrimaryKeyRelatedField(
        queryset=cert.objects.only("cert_name", "cert_code", "cert_price"),
        source="certificate",
        write_only=True,
    )

    activate_price = (
        serializers.SerializerMethodField()
    )  # gold_price().get_active_price()

    gold_price_summary = serializers.IntegerField(read_only=True)
    gold_price_summary_roundup = serializers.IntegerField(read_only=True)

    stock = serializers.SerializerMethodField()

    def get_activate_price(self, obj):
        return obj.get_active_price()

    def get_stock(self, obj):
        return obj.cert_detail_count - obj.open_order_count

    class Meta:
        model = gold
        fields = [
            "gold_id",
            "gold_weight",
            "type",
            "brand",
            "certificate",
            "activate_price",
            "redeem_price",
            "certificate_id",
            "certificate_weight",
            "product_cost",
            "stock",
            "gold_image_1",
            "gold_image_2",
            "gold_image_3",
            "gold_image_4",
            "gold_image_5",
            "gold_price_summary",
            "gold_price_summary_roundup",
        ]
        read_only_fields = [
            "gold_id",
        ]


class GoldServiceFilter(filters.FilterSet):
    class Meta:
        model = gold

        fields = {
            "type": ["icontains"],
            "brand": ["icontains"],
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

    def create(self, validated_data):
        goldPriceConfig = gold_price_config.objects.create(
            **validated_data,
            create_user=self.context["request"].user.id,
            create_time=datetime.now(),
            create_user_email=self.context["request"].user.email,
            upd_user=self.context["request"].user.id,
            upd_time=datetime.now(),
            upd_user_email=self.context["request"].user.email,
        )

        return goldPriceConfig

    def update(self, instance: gold_price_config, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.upd_user = self.context["request"].user.id
        instance.upd_time = datetime.now()
        instance.upd_user_email = self.context["request"].user.email
        instance.save()

        return instance


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
            "gold_price_buy_round",
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


# end region


# region Cert Price Config
class GoldCertPriceSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_cert_detail_price
        fields = [
            "id",
            "gold",
            "gold_cert",
            "gold_cert_code",
            "gold_weight",
            "include_stock",
            "create_time",
            "create_user",
            "create_user_email",
            "upd_time",
            "upd_user",
            "upd_user_email",
        ]
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        goldCert = gold_cert_detail_price.objects.create(
            **validated_data,
            create_user=self.context["request"].user.id,
            create_time=datetime.now(),
            create_user_email=self.context["request"].user.email,
            upd_user=self.context["request"].user.id,
            upd_time=datetime.now(),
            upd_user_email=self.context["request"].user.email,
        )
        return goldCert

    def update(self, instance: gold_cert_detail_price, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.upd_user = self.context["request"].user.id
        instance.upd_time = datetime.now()
        instance.upd_user_email = self.context["request"].user.email
        instance.save()

        return super().update(self.instance, validated_data)


class GoldCertPriceServiceFilter(filters.FilterSet):
    class Meta:
        model = gold_cert_detail_price

        fields = {
            "gold_cert_code": ["icontains"],
            "gold_id": ["exact"],
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

    def create(self, validated_data):

        goldPromoModel = gold_promo.objects.create(
            **validated_data,
            create_user=self.context["request"].user.id,
            create_time=datetime.now(),
            create_user_email=self.context["request"].user.email,
            upd_user=self.context["request"].user.id,
            upd_time=datetime.now(),
            upd_user_email=self.context["request"].user.email,
        )
        return goldPromoModel

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.upd_user = self.context["request"].user.id
        instance.upd_time = datetime.now()
        instance.upd_user_email = self.context["request"].user.email
        instance.save()

        return super().update(self.instance, validated_data)


class GoldPromoFilter(filters.FilterSet):
    class Meta:
        model = gold_promo

        fields = {
            "gold_promo_code": ["icontains"],
            "gold_promo_description": ["icontains"],
        }


# end region
