from os import read
from attr import validate
from rest_framework import serializers
from wallet.models import topup_transaction
from shared_kernel.services.external.xendit_service import (
    QRISPaymentService,
    VAPaymentService,
)
from core.domain import bank
from user.models.users import user_virtual_account as UserVa
from datetime import datetime, timedelta
from uuid import uuid4
import json


class TopupVASerializer(serializers.ModelSerializer):
    class Meta:
        model = topup_transaction
        fields = [
            "topup_total_amount",
            "topup_admin",
            "topup_amount",
            "topup_payment_method",
            "topup_payment_bank_name",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if data["topup_total_amount"] != data["topup_admin"] + data["topup_amount"]:
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )

        # check if va is still in pending phased or not
        user = self.context["request"].user
        userVa = UserVa.objects.filter(user=user).first()
        if (
            userVa
            and topup_transaction.objects.filter(
                topup_payment_number=userVa.va_number, topup_status="PENDING"
            ).exists()
        ):
            raise serializers.ValidationError(
                "Please wait until your Va transaction is done."
            )
        return data

    def create(self, validated_data, **kwargs):
        bank_code = validated_data["topup_payment_bank_name"]
        user = self.context["request"].user  # Get the authenticated user
        validated_data["user"] = user
        userVa = UserVa.objects.filter(user=user).first()
        coreBank = bank.objects.get(bank_merchant_code=bank_code)
        virtual_account_number = (
            f"{coreBank.bank_create_code_va}{userVa.va_number[len(userVa.merchant_code):]}"
            if userVa
            else f"{coreBank.bank_create_code_va}{coreBank.generate_va()}"
        )
        # create va if va is not avail
        service = VAPaymentService()
        # Generate static VA
        payload = service.generate_payload(
            float(validated_data["topup_total_amount"]),
            f"va_generated_user_{user.id}_{str(uuid4())}",
            bank_code,
            user,
            virtual_account_number,
        )

        payload_json = json.dumps(payload)
        virtual_account = service.va_payment_generate(payload_json)
        if not virtual_account:
            raise serializers.ValidationError("Failed to process VA payment.")

        if not userVa:
            userVa = UserVa.objects.create(
                user=user,
                bank=bank_code,
                va_number=virtual_account.get("account_number").removeprefix(
                    virtual_account.get("merchant_code")
                ),
                merchant_code=virtual_account.get("merchant_code"),
            )

        validated_data["topup_payment_method"] = "VA"
        validated_data["topup_payment_channel_code"] = virtual_account.get(
            "channel_code"
        )
        validated_data["topup_payment_number"] = str(virtual_account.get("id"))
        validated_data["topup_payment_expires_at"] = virtual_account.get("expires_at")
        validated_data["topup_payment_ref"] = virtual_account.get("external_id")
        validated_data["topup_payment_ref_code"] = virtual_account.get("account_number")

        self.context["response"] = {
            "total_amount": validated_data["topup_total_amount"],
            "va_number": virtual_account.get("account_number"),
            "reference_id": virtual_account.get("external_id"),
        }

        return super().create(validated_data, **kwargs)


class TopupQrisSerializer(serializers.ModelSerializer):

    class Meta:
        model = topup_transaction
        fields = [
            "topup_total_amount",
            "topup_admin",
            "topup_amount",
            "topup_payment_method",
        ]

    def validate(self, data):
        # Ensure the total amount is the sum of amount and admin fees
        if data["topup_total_amount"] != data["topup_admin"] + data["topup_amount"]:
            raise serializers.ValidationError(
                "Total amount must equal the sum of admin fees and top-up amount."
            )
        # validate amount is not more than 10 m
        if data["topup_total_amount"] > 10000000:
            raise serializers.ValidationError(
                "Total amount must be less than 10 million."
            )

        return data

    def create(self, validated_data, **kwargs):
        user = self.context["request"].user  # Get the authenticated user
        validated_data["user"] = user

        qris = validated_data["topup_payment_method"]
        service = QRISPaymentService()
        # Generate static VA

        payload = service.generate_payload(
            validated_data["topup_total_amount"],
            f"qris_generated_user_{user.id}_{str(uuid4())}",
        )
        payload_json = json.dumps(payload)
        qris = service.qris_payment_generate(payload_json)
        if not qris:
            raise serializers.ValidationError("Failed to process QRIS payment.")
        print(qris, "qris")

        validated_data["topup_payment_method"] = "QRIS"
        validated_data["topup_payment_channel_code"] = qris.get("channel_code")
        validated_data["topup_payment_number"] = str(qris.get("id"))
        validated_data["topup_payment_expires_at"] = qris.get("expires_at")
        validated_data["topup_payment_ref"] = qris.get("reference_id")
        validated_data["topup_payment_ref_code"] = qris.get("qr_string")

        # topup_transaction.objects.create(**validated_data)

        self.context["response"] = {
            "total_amount": validated_data["topup_total_amount"],
            "qr_string": qris.get("qr_string"),
            "reference_id": qris.get("reference_id"),
        }

        return super().create(validated_data, **kwargs)
