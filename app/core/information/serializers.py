"""
Serializer for recipe api
"""

from rest_framework import serializers

from core.models import (
    information_educational, 
    information_promo, 
    information_customer_service,
    information_rating,) 

class InformationCustomerServiceSerializer(serializers.ModelSerializer):
    """Serializer for recipe object"""

    class Meta:
        model = information_customer_service
        fields = ['information_customer_service_id', 'information_phone', 'information_name']
        read_only_fields = ['information_customer_service_id',]
        
        
class InformationEducationalSerializer(serializers.ModelSerializer):
    """Serializer for Information Rating Educational object"""

    class Meta:
        model = information_educational
        fields = "__all__"
        read_only_fields = ['id',]
        
class InformationPromoSerializer(serializers.ModelSerializer):
    """Serializer for information Promo object"""

    class Meta:
        model = information_promo
        fields = "__all__"
        read_only_fields = ['id',]
        
        
class InformationRatingSerializer(serializers.ModelSerializer):
    """Serializer for information Rating object"""

    class Meta:
        model = information_rating
        fields = "__all__"
        read_only_fields = ['id',]