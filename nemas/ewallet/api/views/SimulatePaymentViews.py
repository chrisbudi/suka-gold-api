from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ewallet.api.serializers import (
    SimulatedPaymentVaSerializer as modelVASerializer,
    SimulatedPaymentQrisSerializer as modelqrisSerializer,
)


@extend_schema(
    tags=["Topup - Topup Transaction Create"],
)
class SimulatePaymentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=modelVASerializer,
        responses={200: modelVASerializer},
    )
    def simulate_payment_qris(self, request):
        serializer = modelqrisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=modelVASerializer,
        responses={200: modelVASerializer},
    )
    def simulate_payment_va(self, request):
        serializer = modelqrisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
