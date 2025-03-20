from rest_framework.decorators import api_view
from core.gold.api.serializers import (
    GoldPromoSerializer as modelSerializer,
    GoldPromoFilter as modelFilter,
)
from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.domain import gold_promo as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["gold promo"],
)
class GoldPromoViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = modelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = modelFilter

    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = modelSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = modelSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = modelSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = modelSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        info.delete()
        return response.Response(
            {
                "message": "Information Rating deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
