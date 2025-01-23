from locale import currency
from math import exp
from os import name
import time
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from shared_kernel.services.external.xendit_service import (
    VAPaymentService as vaService,
    QRISPaymentService as qrisService,
)
from ewallet.api.serializers import (
    TopupVASerializer as modelVASerializer,
    TopupQrisSerializer as modelqrisSerializer,
)
import uuid
from user.models import user_virtual_account as UserVA
from core.domain import bank as Bank
from ewallet.models import topup_transaction as TopupTransaction


@extend_schema(
    tags=["Topup - Topup Transaction Create"],
)
class TopupTransactionView(viewsets.ModelViewSet):
    serializer_class = modelVASerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def generate_va(self, request):
        serializer = modelVASerializer(data=request.data)
        if serializer.is_valid():
            # check if user has virtual accoount if not have create one
            bank_code = serializer.validated_data["topup_payment_bank"]
            user = request.user
            userVa = UserVA.objects.filter(user=user, bank=bank_code).first()
            bank = Bank.objects.get(bank_merchant_code=bank_code)
            # create va if va is not avail
            if not userVa:
                service = vaService()
                # Generate static VA
                payload = {
                    "external_id": "va_generated_user_" + user.id,
                    "bank_code": bank_code,
                    "name": user.name,
                    "virtual_account_number": bank.generate_va(),
                }
                virtual_account = service.va_payment_generate(payload)
                userVa = UserVA.objects.create(
                    user=user,
                    bank=bank_code,
                    account_number=virtual_account["account_number"],
                    owner_id=virtual_account["owner_id"],
                    merchant_code=virtual_account["merchant_code"],
                    expiration_date=virtual_account["expiration_date"],
                )
                userVa.save()
            # Save to database

            serializer.save(userVa=userVa)

            data = {
                "total_amount": serializer.validated_data["toup_total_amount"],
                "user_virtual_account": userVa.va_number,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def simulate_payment_va(self, request):
        serializer = modelVASerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            userVa = UserVA.objects.filter(user=user).first()
            if not userVa:
                return Response(
                    {"error": "User does not have virtual account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            service = vaService()
            payload = {
                "external_id": "va_generated_user_" + user.id,
                "bank_code": userVa.bank,
                "name": user.name,
                "account_number": userVa.va_number,
                "amount": serializer.validated_data["topup_total_amount"],
            }
            virtual_account = service.va_payment_simulate(payload)
            data = {
                "total_amount": serializer.validated_data["toup_total_amount"],
                "user_virtual_account": userVa.va_number,
                "payment_status": virtual_account["status"],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_qris(self, request):
        serializer = modelqrisSerializer(data=request.data)
        if serializer.is_valid():
            # check if user has virtual accoount if not have create one
            qris = serializer.validated_data["topup_payment_ref"]
            user = request.user

            service = qrisService()
            # Generate static VA
            payload = {
                "external_id": "qris_generated_user_" + user.id + "_" + uuid.uuid4(),
                "type": "DYNAMIC",
                "currency": "IDR",
                "amount": serializer.validated_data["topup_total_amount"],
                "expires_at": time.time() + 7200,  # 2 hours in seconds
                "channel_code": "ID_DANA",
            }
            qris = service.qris_payment_generate(payload)

            serializer.save(
                user=user,
                topup_payment_ref=qris["qr_string"],
                external_id=payload["external_id"],
            )

            data = {
                "total_amount": payload["toup_total_amount"],
                "user_virtual_account": qris["qr_string"],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def simulate_payment_qris(self, request):
        serializer = modelqrisSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            service = qrisService()
            payload = {
                "external_id": "qris_generated_user_" + user.id + "_" + uuid.uuid4(),
                "type": "DYNAMIC",
                "currency": "IDR",
                "amount": serializer.validated_data["topup_total_amount"],
                "expires_at": time.time() + 7200,  # 2 hours in seconds
                "channel_code": "ID_DANA",
            }
            qris = service.qris_payment_simulate(payload)
            data = {
                "total_amount": serializer.validated_data["toup_total_amount"],
                "user_virtual_account": qris["qr_string"],
                "payment_status": qris["status"],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
