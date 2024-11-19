"""
Serializers for user api view
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import user_props


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ("email", "phone_number", "password", "name")
        extra_kwargs = {"password": {"min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        # build user props
        print("user", user)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.save()
        return user


class AuthTokenObtainPairSerializer(serializers.Serializer):
    # Override fields to use identifier instead of username
    identifier = serializers.CharField()
    password = serializers.CharField(trim_whitespace=True, write_only=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        # Authenticate user based on identifier (username/email/phone)
        user = authenticate(
            request=self.context.get("request"), username=identifier, password=password
        )

        if user is None:
            msg = "Unable to authenticate with provided credentials."
            raise serializers.ValidationError(msg, code="authentication")

        # If user is authenticated, proceed to generate tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
