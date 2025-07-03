from rest_framework import serializers
from shared.services.external.delivery.sapx.sapx_service import SapxService
from order.models import order_shipping


class OrderShippingSerializer(serializers.Serializer):
    # list_of_cart_detail_id = serializers.ListField(child=serializers.IntegerField())
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)
    weight = serializers.DecimalField(max_digits=10, decimal_places=4)
    delivery_partner_code = serializers.ChoiceField(
        choices=["PAXEL", "SAPX"], required=True
    )

    def validate(self, data):

        return data

    def create(self, validated_data):

        return super().create(validated_data)


class OrderShippingAssignSerializer(serializers.Serializer):

    class Meta:
        model = order_shipping
        fields = [
            "gold_id",
            "quantity",
        ]

    def validate(self, data):

        return data

    def create(self, validated_data):

        return super().create(validated_data)
