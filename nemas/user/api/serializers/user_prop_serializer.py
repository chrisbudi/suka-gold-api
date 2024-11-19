from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import (
    user_props,
)


class UserPropSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = user_props
        fields = (
            "wallet_amt",
            "gold_wgt",
            "invest_gold_wgt",
            "loan_wgt",
            "loan_amt",
            "photo",
            "bank",
            "rek_number",
            "level",
            "level_id",
            "address",
            "address_post_code",
            "create_time",
            "create_user",
            "update_time",
            "update_user",
        )
