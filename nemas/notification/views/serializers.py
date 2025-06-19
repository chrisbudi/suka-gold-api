from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(default="", allow_blank=True)
    message = serializers.CharField(default="", allow_blank=True)
    data = serializers.DictField(required=False, allow_null=True, allow_empty=True)
