from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from common.responses import NemasReponses
from order_fix.api.serializers.OrderSimulatePaymentSerializer import (
    OrderSimulatedPaymentQrisSerializer,
    OrderSimulatedPaymentVaSerializer,
)


@extend_schema(
    tags=["Order Fix - Order Payment"],
)
class OrderPaymentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination

    @extend_schema(
        summary="Simulate Payment VA",
        description="Simulate a payment for a virtual account.",
        request=OrderSimulatedPaymentVaSerializer,
        responses={200: OrderSimulatedPaymentVaSerializer},
    )
    def simulate_va_payment(self, request):
        print(request.data, "request.data")

        serializer = OrderSimulatedPaymentVaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            result = serializer.save()
            return response.Response(result, status=status.HTTP_201_CREATED)
        return response.Response(
            NemasReponses.failure("Validation Failed", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Simulate Payment QRIS",
        description="Simulate a payment for a QRIS.",
        request=OrderSimulatedPaymentQrisSerializer,
        responses={200: OrderSimulatedPaymentQrisSerializer},
    )
    def simulate_qris_payment(self, request):
        serializer = OrderSimulatedPaymentQrisSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            result = serializer.save()
            return response.Response(result, status=status.HTTP_201_CREATED)
        return response.Response(
            NemasReponses.failure("Validation Failed", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
