"""
Serializers for user api view
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
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


class AuthenticatedTokenSerializer(serializers.Serializer):
    """Serializer for user authentication"""

    identifier = serializers.CharField()  # Can be username, email, or phone number
    password = serializers.CharField(trim_whitespace=True)
    print("AuthenticatedTokenSerializer", identifier, password)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=identifier, password=password
        )

        if not identifier or not password:
            msg = 'Must include "identifier" and "password".'
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user
        return attrs

        # user = authenticate(
        #     request=self.context.get('request'),
        #     username=email,
        #     password=password
        # )

        # if not user:
        #     msg = ('Unable to authenticate with provided credentials')
        #     raise serializers.ValidationError(msg, code='authentication')

        # attrs['user'] = user
        # return attrs
