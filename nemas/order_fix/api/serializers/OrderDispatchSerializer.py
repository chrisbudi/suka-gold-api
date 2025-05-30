from rest_framework import serializers
import json


class OrderDispatchSerializer(serializers.Serializer):
    # list_of_cart_detail_id = serializers.ListField(child=serializers.IntegerField())
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    weight = serializers.DecimalField(max_digits=10, decimal_places=4)

    def validate(self, data):

        return data

    def create(self, validated_data):

        return super().create(validated_data)
