from investment.api.serializers import (
    TransactionSerializer as customSerializer,
    TransactionFilter as customFilter,
)
from rest_framework import status, viewsets, filters, pagination, response
from investment.models import TransactionModel as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated

# Removed unused import


@extend_schema(
    tags=["deposito transaction - service "],
)
class TransactionServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = customSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = customFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    @extend_schema(
        summary="List deposito transactions",
        description="Retrieve a list of deposito transactions for the authenticated user.",
        responses={200: customSerializer},
    )
    def list(self, request):
        queryset = modelInfo.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = customSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create deposito transaction",
        description="Create a deposito transaction for the authenticated user.",
        request=customSerializer,
        responses={201: customSerializer},
    )
    def perform_create(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
