from rest_framework import serializers


class OrderShippingSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)

    def validate(self, data):
        amount = data.get("amount")
        reference_id = data.get("reference_id")
        if amount:
            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

        print(reference_id, "reference_id")
        if not reference_id:
            raise serializers.ValidationError("Reference ID is need")

        return data
