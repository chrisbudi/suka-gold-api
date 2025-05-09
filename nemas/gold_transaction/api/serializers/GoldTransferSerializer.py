from rest_framework import serializers
from gold_transaction.models import gold_transfer
from django_filters import rest_framework as filters
from datetime import datetime
from common.generator import generate_alphanumeric_code
from user.models import user_props, user


class GoldTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = gold_transfer
        fields = [
            "gold_transfer_id",
            "phone_number",
            "transfer_member_gold_weight",
            "transfer_ref_number",
            "transfer_member_notes",
        ]
        read_only_fields = ["gold_transfer_id"]

    def validate(self, attrs):
        # validate if phone number is valid
        if not user.objects.filter(phone_number=attrs["phone_number"]).exists():
            raise serializers.ValidationError("Phone number is not valid")
        # validate if user is not the same
        if (
            user.objects.get(phone_number=attrs["phone_number"])
            == self.context["request"].user
        ):
            raise serializers.ValidationError("Cannot transfer to yourself")
        # validate balance is enough

        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_weight(attrs["transfer_member_gold_weight"]):
            raise serializers.ValidationError("Balance is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        # Calculate total price before saving
        validated_data["transfer_member_datetime"] = datetime.now()
        validated_data["user_from"] = self.context["request"].user

        # generate number for transaction
        gold_transfer_number = (
            "TM" + datetime.now().strftime("%y%m") + generate_alphanumeric_code()
        )
        validated_data["transfer_ref_number"] = (
            gold_transfer_number
            if self.instance is None
            else self.instance.transfer_ref_number
        )

        # from user phone number to user
        user_to = user.objects.get(phone_number=validated_data["phone_number"])
        validated_data["user_to"] = user_to

        # print(validated_data, "validated data")
        return super().create(validated_data)


class GoldTransferFilter(filters.FilterSet):
    class Meta:
        model = gold_transfer

        fields = {
            "transfer_member_datetime": ["lte", "gte"],
        }
