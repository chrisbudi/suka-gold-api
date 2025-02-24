from attr import validate
from rest_framework import serializers
from shared_kernel.services.external.sapx_service import SapxService
import json


class OrderShippingSerializer(serializers.Serializer):
    list_of_cart_detail = serializers.CharField(max_length=50)

    def validate(self, data):

        return data

    def create(self, validated_data):
        sapx_service = SapxService()

        payload = {
            "origin": "DEV",
            "destination": "DEV",
            "weight": 1,
            "customer_code": "DEV000",
            "packing_type_code": "ACH05",
            "volumetric": "1x1x1",
            "insurance_type_code": "INS02",
            "item_value": validated_data.get("amount"),
        }
        payload_data = json.dumps(payload)
        data = sapx_service.get_price(payload_data)

        return super().create(validated_data)
