from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models.users import user_address


class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = user_address
        fields = (
            "id",
            "address",
            "city",
            "district",
            "province",
            "subdistrict",
            "postal_code",
            "is_default",
            "longtitude",
            "latitude",
        )
