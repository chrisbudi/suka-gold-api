"""
Serializers for user api view
"""

from django.contrib.auth import get_user_model
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers


class UserVerificationSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # create user prop

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        # print(password, "password");
        if password:
            user.set_password(password)
            user.save()

        return user
