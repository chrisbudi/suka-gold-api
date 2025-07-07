from rest_framework import serializers


class ContactRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    message = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
