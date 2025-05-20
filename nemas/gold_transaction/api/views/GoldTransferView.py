from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_transfer
from gold_transaction.api.serializers import GoldTransferSerializer, GoldTransferFilter
from decimal import Decimal, InvalidOperation


@extend_schema(
    tags=["gold transaction - Gold Transfer"],
)
class GoldTransferListCreateAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = gold_transfer.objects.all()  # Use the model class directly
    serializer_class = GoldTransferSerializer
    authentication_classes = [JWTAuthentication]
    filterset_class = GoldTransferFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination

    @extend_schema(
        summary="List Gold Transfer",
        description="Retrieve a list of gold Transfer for the authenticated user.",
        responses={200: GoldTransferSerializer},
    )
    def list(self, request):
        queryset = gold_transfer.objects.filter(user_from=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldTransferSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Calculate Gold Transfer Weight",
        description="Calculate and return the gold transfer weight for the authenticated user.",
        request={
            "application/json": {
                "type": "object",
                "properties": {"weight": {"type": "number"}},
                "required": ["weight"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "weight": {"type": "number"},
                    "weight_cost": {"type": "number"},
                },
            }
        },
    )
    def calculate_weight(self, request):
        weight = request.data.get("weight")
        if weight is not None:
            gold_transfer_instance = gold_transfer()
            transfer_cost = round(gold_transfer_instance.get_transfer_cost(weight), 4)
            return response.Response(
                {
                    "weight_transfered": round(weight - transfer_cost, 4),
                    "transfer_cost": round(transfer_cost, 4),
                }
            )
        else:
            return response.Response(
                {"error": "Weight must be a valid decimal number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        summary="Create Gold Transfer",
        description="Create a gold Transfer for the authenticated user.",
        request=GoldTransferSerializer,
        responses={201: GoldTransferSerializer},
    )
    def perform_create(self, request):
        serializer = GoldTransferSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
