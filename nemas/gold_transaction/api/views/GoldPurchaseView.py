from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Correct model import
from gold_transaction.models import gold_saving_buy
from gold_transaction.api.serializers import (
    GoldTransactionBuySerializer,
    GoldTransactionBuyFilter,
)


@extend_schema(
    tags=["gold transaction - Gold Purchase"],
)
class GoldPurchaseListCreateAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = gold_saving_buy.objects.all()  # Use the model class directly
    serializer_class = GoldTransactionBuySerializer
    authentication_classes = [JWTAuthentication]
    filterset_class = GoldTransactionBuyFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed
    search_fields = ["transaction_date", "weight", "price_per_gram", "total_price"]

    @extend_schema(
        summary="List Gold Purchases",
        description="Retrieve a list of gold purchases for the authenticated user.",
        responses={200: GoldTransactionBuySerializer},
    )
    def list(self, request):
        queryset = gold_saving_buy.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldTransactionBuySerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create Gold Purchase",
        description="Create a gold purchase for the authenticated user.",
        request=GoldTransactionBuySerializer,
        responses={201: GoldTransactionBuySerializer},
    )
    def perform_create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
