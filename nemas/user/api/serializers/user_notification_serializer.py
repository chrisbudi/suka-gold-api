from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
import user
from user.models import user_notification_price
from user.models import user_notification

from django_filters import rest_framework as filters
from datetime import datetime


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
        )

        read_only_fields = (
            "user_notification_price_id",
            "timestamps",
            "user_notification_price_status",
        )

    def create(self, validated_data):

        print(validated_data, "validated_data")

        notification_price = user_notification_price.objects.create(
            **validated_data,
            user=self.context["request"].user,
            timestamps=datetime.now(),
        )
        return notification_price

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.timestamps = datetime.now()
        instance.user = self.context["request"].user
        instance.save()
        return instance

    # on update update user and timestamps


class UserNotificationFilterSerializer(filters.FilterSet):
    class Meta:
        model = user_notification

        fields = {
            "user_notification_title": ["icontains"],
        }
