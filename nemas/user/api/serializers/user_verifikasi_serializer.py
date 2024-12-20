from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import (
    user_ktp,
)


class UserVerifikasiSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_ktp
        fields = ()

    # def create(self, validated_data):
    #     """Create a new user with encrypted password and return it"""
    #     return get_user_model().objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     """Update a user, setting the password correctly and return it"""
    #     password = validated_data.pop("password", None)
    #     user = super().update(instance, validated_data)

    #     if password:
    #         user.set_password(password)
    #         user.save()

    #     return user
