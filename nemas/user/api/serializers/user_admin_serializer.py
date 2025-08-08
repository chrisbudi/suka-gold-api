"""
Serializers for user api view
"""

from django.contrib.auth import get_user_model
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from django_filters import rest_framework as filters

from common.generator import generate_numeric_code
from user.models.users import role, user_address, user_ktp, user_props


class user_ktp_serializer(serializers.ModelSerializer):

    class Meta:
        model = user_ktp
        fields = (
            "nik",
            "full_name",
            "date_of_birth",
            "place_of_birth",
            "address",
            "district",
            "administrative_village",
            "gender",
            "religion",
            "marital_status",
            "occupation",
            "nationality",
            "city",
            "blood_type",
            "reference_id",
        )

        read_only_fields = ("id",)


class user_props_serializer(serializers.ModelSerializer):
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
            "bank_account_code",
            "bank_account_number",
            "bank_account_holder_name",
            "level",
            "level_id",
            "address",
            "address_post_code",
            "create_time",
            "create_user",
        )


class user_address_serializer(serializers.ModelSerializer):
    """Serializer for the user address object"""

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
        read_only_fields = ("id",)


class UserAdminSerializer(serializers.ModelSerializer):
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
    # load from user_ktp serializer
    ktp = user_ktp_serializer(
        required=False, allow_null=True, read_only=True, source="user_ktp"
    )

    props = user_props_serializer(
        required=False, allow_null=True, read_only=True, source="user_props"
    )

    address = user_address_serializer(
        required=False, allow_null=True, read_only=True, source="user_address"
    )
    role_name = serializers.CharField(
        source="role.name", read_only=True, allow_blank=True, max_length=255
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=role.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "member_number",
            "user_name",
            "email",
            "phone_number",
            "password",
            "name",
            "role",
            "role_name",
            "income_source",
            "investment_purpose",
            "referal_code",
            "ktp",
            "props",
            "address",
        ]

        read_only_fields = (
            "id",
            "member_number",
            "is_2fa_verified",
            "is_active",
            "is_verified",
            "is_ktp_verified",
            "is_email_verified",
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

    def delete(self, instance):
        """Custom delete to set is_deleted=True instead of actual deletion"""
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
        return instance


# class filter
class UserAdminServiceFilter(filters.FilterSet):
    """Filter for the user admin view"""

    class Meta:
        model = get_user_model()
        fields = {
            "id": ["exact"],
            "email": ["exact", "icontains"],
            "user_name": ["exact", "icontains"],
            "phone_number": ["exact", "icontains"],
            "name": ["exact", "icontains"],
            "member_number": ["exact", "icontains"],
            "role__name": ["exact", "icontains"],
            "is_active": ["exact"],
        }
