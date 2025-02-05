from rest_framework import serializers
from gold_transaction.models import gold_transfer
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from user.models import user_props

User = get_user_model()


class GoldTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = gold_transfer
        fields = [
            "gold_transfer_id",
            "user_to",
            "transfer_member_gold_weight",
            "transfer_ref_number",
            "transfer_member_notes",
            "transfer_member_datetime",
        ]
        read_only_fields = ["gold_transfer_id"]

    def validate(self, attrs):
        # validate balance is enough

        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_weight(attrs["price"]):
            raise serializers.ValidationError("Balance is not enough")
        return super().validate(attrs)

    def get_user_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        # Calculate total price before saving
        validated_data["transfer_member_datetime"] = datetime.now()
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class GoldTransferFilter(filters.FilterSet):
    class Meta:
        model = gold_transfer

        fields = {
            "transfer_member_datetime": ["lte", "gte"],
        }
