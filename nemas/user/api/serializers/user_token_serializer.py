"""
Serializers for user api view
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import user_reset_token


class UserTokenSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        # create serializer for email accept email
        model = user_reset_token
        fields = ("id", "user", "token", "created_at")
        extra_kwargs = {"token": {"write_only": True, "min_length": 5}}


class EmailSerializer(serializers.Serializer):
    """Serializer for request email"""

    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):
    """Serializer for request email"""

    Token = serializers.CharField()
