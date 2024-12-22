from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import (
    user_ktp,
)


class UserKtpSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_ktp
        fields = (
            "nik",
            "full_name",
            "date_of_birth",
            "place_of_birth",
            "address",
            "district",
            "adminitrative_village",
            "gender",
            "religion",
            "marital_status",
            "occupation",
            "nationality",
            "photo_url",
            "city",
        )


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value
