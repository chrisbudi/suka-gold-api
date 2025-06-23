from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import user_notification_price
from user.models import user_notification

from django_filters import rest_framework as filters


class UserNotificationSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = user_notification
        fields = (
            "user_notification_id",
            "user_notification_title",
            "user_notification_description",
            "user_notification_date",
            "user_notification_icon_type",
            "user",
        )


class UserNotificationPriceSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = user_notification_price
        fields = (
            "user_notification_price_id",
            "user_notification_price_buy",
            "user_notification_price_sell",
            "timestamps",
            "user_notification_price_status",
            "user",
        )


class UserNotificationFilterSerializer(filters.FilterSet):
    class Meta:
        model = user_notification

        fields = {
            "user_notification_title": ["icontains"],
        }
