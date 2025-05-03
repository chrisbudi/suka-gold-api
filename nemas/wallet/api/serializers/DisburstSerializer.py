from attr import validate
from rest_framework import serializers
from common.generator import generate_alphanumeric_code
from shared_kernel.services.external.xendit_service.disbursment_service import (
    DisburstService,
)
from wallet.models import disburst_transaction
from core.domain import bank
from user.models import user_props
from user.models.users import user_virtual_account as UserVa
from datetime import datetime, timedelta
from uuid import uuid4
import json


class DisburstSerializer(serializers.ModelSerializer):
    class Meta:
        model = disburst_transaction
        fields = [
            "disburst_total_amount",
            "disburst_admin",
            "disburst_amount",
            "disburst_payment_bank_code",
            "disburst_payment_bank_number",
            "disburst_payment_bank_account_holder_name",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if (
            data["disburst_total_amount"]
            != data["disburst_admin"] + data["disburst_amount"]
        ):
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )

        # ensure user saldo is more than total amount
        if not user_props.objects.get(
            user=self.context["request"].user
        ).validate_balance(data["disburst_total_amount"]):
            raise serializers.ValidationError("Balance is not enough")

        # check if va is still in pending phased or not
        user = self.context["request"].user
        userVa = UserVa.objects.filter(user=user).first()

        return data

    def create(self, validated_data, **kwargs):
        user = self.context["request"].user  # Get the authenticated user
        validated_data["user"] = user
        # userVa = UserVa.objects.filter(user=user).first()
        # coreBank = bank.objects.get(bank_merchant_code=bank_code)
        # # create va if va is not avail
        service = DisburstService()
        # # Generate static VA
        payload = {
            "external_id": f"disb_{user.id}_{str(uuid4())}",
            "amount": float(validated_data["disburst_total_amount"]),
            "bank_code": validated_data["disburst_payment_bank_code"],
            "account_number": validated_data["disburst_payment_bank_number"],
            "account_holder_name": validated_data[
                "disburst_payment_bank_account_holder_name"
            ],
            "description": "Disburstment",
        }

        payload_json = json.dumps(payload)
        disburst = service.disburst_generate(payload_json)
        if disburst is None:
            raise serializers.ValidationError("Failed to process Disburstment.")

        # generate disburst number
        disburst_number = (
            "TU/" + datetime.now().strftime("%y%m") + "/" + generate_alphanumeric_code()
        )
        validated_data["disburst_number"] = (
            disburst_number if self.instance is None else self.instance.disburst_number
        )
        validated_data["disburst_timestamp"] = datetime.now()
        validated_data["disburst_payment_ref"] = disburst.get("id")
        self.context["response"] = {
            "amount": disburst["amount"],
            "bank_code": disburst.get("bank_code"),
            "account_holder_name": disburst.get("account_holder_name"),
        }

        return super().create(validated_data, **kwargs)
