from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_saving_buy
from common.responses import NemasReponses
from order_fix.api.serializers.OrderGoldSerializer.order_gold import (
    OrderGoldSerializer,
    OrderGoldListSerializer,
    SubmitOrderGoldSerializer,
)
from order_fix.api.serializers.OrderSimulatePaymentSerializer import (
    OrderSimulatedPaymentQrisSerializer,
    OrderSimulatedPaymentVaSerializer,
)

from order.models import order_gold


@extend_schema(
    tags=["Order Fix - Order Gold"],
)
class OrderGoldAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = gold_saving_buy.objects.all()  # Use the model class directly
    serializer_class = OrderGoldSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    @extend_schema(
        summary="List Order Gold",
        description="Retrieve a list of order gold purchases for the authenticated user.",
        responses={200: OrderGoldListSerializer},
    )
    def list(self, request):
        queryset = order_gold.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = OrderGoldListSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create Gold Purchase",
        description="Create a order gold purchase for the authenticated user.",
        request=SubmitOrderGoldSerializer,
        responses={201: OrderGoldSerializer},
    )
    def perform_create(self, request):
        serializer = SubmitOrderGoldSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            result = serializer.save()
            print(result, "result serializer")
            return response.Response(result, status=status.HTTP_201_CREATED)
        return response.Response(
            NemasReponses.failure("Validation Failed", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Simulate Payment VA",
        description="Simulate a payment for a virtual account.",
        request=OrderSimulatedPaymentVaSerializer,
        responses={200: OrderSimulatedPaymentVaSerializer},
    )
    def simulate_va_payment(self, request, pk: str):
        print(request.data, "request.data", pk)

        serializer = OrderSimulatedPaymentVaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            print(serializer, "serializer")
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
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
    def simulate_qris_payment(self, request, pk: str):
        serializer = OrderSimulatedPaymentQrisSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.context.get("response"), status=status.HTTP_201_CREATED
            )
        return response.Response(
            NemasReponses.failure("Validation Failed", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
