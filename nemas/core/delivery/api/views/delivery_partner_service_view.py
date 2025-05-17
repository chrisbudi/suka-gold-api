from core.delivery.api.serializers import (
    DeliveryPartnerServiceSerializer as customSerializer,
    DeliveryPartnerServiceFilter as customFilter,
)
from rest_framework import status, viewsets, filters, pagination, response
from core.domain import delivery_partner_service as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated

# Removed unused import


@extend_schema(
    tags=["delivery partner - service "],
)
class DeliveryPartnerServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = customSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = customFilter
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
        queryset = modelInfo.objects.filter(is_deleted=False)
        if request.query_params.get("delivery_partner_id"):
            queryset = queryset.filter(
                delivery_partner=request.query_params.get("delivery_partner_id")
            )
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = customSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, _, id=None):
        info = get_object_or_404(modelInfo, pk=id)
        serializer = customSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, id=None):
        info = get_object_or_404(modelInfo, pk=id)
        serializer = customSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, _, id=None):  # Unused 'request' replaced with '_'
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        info.delete()
        return response.Response(
            {
                "message": "Information customer service deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
