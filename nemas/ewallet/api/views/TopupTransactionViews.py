from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from shared_kernel.services.external.xendit_service import (
    VAPaymentService as vaService,
    QRISPaymentService as qrisService,
)
from ewallet.api.serializers import (
    TopupVASerializer as modelVASerializer,
    TopupQrisSerializer as modelqrisSerializer,
    SimulatedPaymentSerializer as modelSimulatedPaymentSerializer,
)
from user.models import user_virtual_account as UserVA
from ewallet.models import topup_transaction as TopupTransaction


@extend_schema(
    tags=["Topup - Topup Transaction Create"],
)
class TopupTransactionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=modelVASerializer,
        responses={201: modelVASerializer},
    )
    def generate_va(self, request):
        serializer = modelVASerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.context.get("response"), status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=modelSimulatedPaymentSerializer,
        responses={200: modelVASerializer},
    )
    def simulate_payment_va(self, request, reference_id):
        serializer = modelVASerializer(data=request.data, context={"request": request})
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
            virtual_account = service.va_payment_simulate(reference_id, payload)
            data = {
                "total_amount": serializer.validated_data["topup_total_amount"],
                "user_virtual_account": userVa.va_number,
                "payment_status": virtual_account["status"],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=modelqrisSerializer,
        responses={200: modelVASerializer},
    )
    def generate_qris(self, request):
        serializer = modelqrisSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.context.get("response"), status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=modelSimulatedPaymentSerializer,
        responses={200: modelVASerializer},
    )
    def simulate_payment_qris(self, request, reference_id):
        serializer = modelqrisSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            service = qrisService()
            payload = {
                "amount": serializer.validated_data["topup_total_amount"],
            }
            qris = service.qris_payment_simulate(reference_id, payload)
            data = {
                "total_amount": serializer.validated_data["toup_total_amount"],
                "user_virtual_account": qris["qr_string"],
                "payment_status": qris["status"],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
