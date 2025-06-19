from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    user_email = serializers.EmailField(
        required=False, allow_null=True, allow_blank=True
    )
    title = serializers.CharField(default="", allow_blank=True)
    message = serializers.CharField(default="", allow_blank=True)
    data = serializers.DictField(required=False, allow_null=True, allow_empty=True)
