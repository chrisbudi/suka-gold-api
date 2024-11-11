from core.information.api.serializers import (
    InformationPromoSerializer as infoSerializer,
    InformationPromoFilter as promoFilter,
)

from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.domain import information_promo as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    tags=["Information - Promo"],
)
class InformationPromoViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = promoFilter

    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = infoSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = infoSerializer(data=request.data)
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
        serializer = infoSerializer(info, data=request.data)
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
                "message": "Information Promo deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
