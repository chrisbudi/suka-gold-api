"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters

from core.models import (
    gold,
    gold_price,
    gold_price_config,
    ) 


#region Gold
class GoldSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold
        fields = ['gold_weight', 'type', 'brand', 'certificate_number', 'create_time', 'create_user', 'upd_time', 'upd_user']
        read_only_fields = ['gold_id',]


class GoldServiceFilter(filters.FilterSet):
    class Meta:
        model = gold

        fields = {
            'type': ['icontains'],
        }
#endregion



#region Gold
class GoldPriceConfigSerializer(serializers.ModelSerializer):
    """Serializer for gold object"""

    class Meta:
        model = gold_price_config
        fields = ['gpc_code', 'gpc_description', 'gold_price_weight', 'gold_price_setting_model', 'gpc_active', 'create_time', 'create_user', 'upd_time', 'upd_user']
        read_only_fields = ['gpc_id',]


class GoldPriceConfigServiceFilter(filters.FilterSet):
    class Meta:
        model = gold_price_config

        fields = {
            'gpc_code': ['icontains'],
            'gpc_description': ['icontains'],
        }
#endregion
