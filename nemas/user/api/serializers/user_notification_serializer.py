from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import user_notification


class UserPropSerializer(serializers.ModelSerializer):
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
