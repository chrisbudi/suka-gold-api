from rest_framework import viewsets, filters, pagination, status, response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, permissions
from gold_transaction.api.serializers.GoldInOutStockSerializer import (
    GoldInOutStockSerializer,
)
from gold_transaction.models.gold_stock import gold_stock_inout
from gold_transaction.repositories.gold_stock_repository import (
    GoldStockRepository,
)


@extend_schema(
    summary="List and create gold stock movements",
    description="Retrieve a list of gold stock movement history for the authenticated user, or create a new gold stock movement entry.",
    tags=["Gold Stock History"],
)
class GoldStockMovementListCreateView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = gold_stock_inout.objects.all()  # Use the model class directly
    serializer_class = GoldStockRepository
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = pagination.LimitOffsetPagination

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoldInOutStockSerializer

    @extend_schema(
        summary="List Gold Movement",
        description="Retrieve a list of gold movements for the authenticated user.",
        responses={200: GoldInOutStockSerializer},
    )
    def list(self, request):
        queryset = gold_stock_inout.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = GoldInOutStockSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
