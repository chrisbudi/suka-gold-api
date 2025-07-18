"""
Serializers for user api view
"""

from attr import validate
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice


from django.core.validators import MaxValueValidator, MinValueValidator

from common.generator import generate_numeric_code
from user.models import user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    income_source = serializers.CharField(
        required=False, allow_blank=True, max_length=255
    )
    investment_purpose = serializers.CharField(
        required=False, allow_blank=True, max_length=255
    )
    referal_code = serializers.CharField(
        required=False, allow_blank=True, max_length=255
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "member_number",
            "user_name",
            "member_number",
            "email",
            "phone_number",
            "password",
            "name",
            "is_2fa_verified",
            "income_source",
            "investment_purpose",
            "referal_code",
        ]
        read_only_fields = (
            "id",
            "member_number",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def validate(self, attrs):
        """Validate the data"""
        if self.context.get("is_superuser", False) and not attrs.get("user_name"):
            raise serializers.ValidationError(
                {"user_name": "This field is required for superusers."}
            )
        return attrs

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        member_number = "IDN-" + generate_numeric_code(5)
        validated_data["member_number"] = member_number

        if self.context.get("is_superuser", False):
            return get_user_model().objects.create_superuser(**validated_data)
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        if not instance.member_number:
            validated_data["member_number"] = "IDN-" + generate_numeric_code(5)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserPinSerializer(serializers.Serializer):
    """Serializer for inserting a user pin"""

    pin = serializers.IntegerField(
        validators=[
            MaxValueValidator(1000000, message="PIN must be 6 digits."),
            MinValueValidator(99999, message="PIN must be 6 digits."),
        ]
    )

    class Meta:
        model = user
        fields = ["pin"]

    def update(self, instance, validated_data):
        print(validated_data, "validated_data")
        instance.pin = validated_data.get("pin", instance.pin)
        instance.save()
        return instance


class UserPinVerifySerializer(serializers.Serializer):
    """Serializer for inserting a user pin"""

    pin = serializers.IntegerField(
        validators=[
            MaxValueValidator(1000000, message="PIN must be 6 digits."),
            MinValueValidator(99999, message="PIN must be 6 digits."),
        ]
    )

    class Meta:
        model = user
        fields = ["pin"]

    def validate(self, data, *args, **kwargs):

        pin = data.get("pin", None)
        userModel = self.instance
        if pin is None:
            raise serializers.ValidationError("PIN is required.")
        # verify the pin if the pin is correct
        if pin and self.instance:
            try:
                # verify the pin
                if self.instance.pin != pin:
                    raise serializers.ValidationError("Invalid PIN.")
            except user.DoesNotExist:
                raise serializers.ValidationError("Invalid user or PIN.")

        return data


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
        if not user or not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials or inactive account"},
                code="authentication",
            )

        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if device:
            raise serializers.ValidationError(
                {"detail": "2FA required", "partial_token": str(user.pk)},
                code="2fa_required",
            )
        # If user is authenticated, proceed to generate tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
