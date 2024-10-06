from core.address.serializers import (
    CitySerializer as customSerializer,
    CityFilter as customFilter,
)
from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.models import city as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    tags=["Address - City "],
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = customSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = customFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    def list(self, request):
        # queryset join from province and city
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = customSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = customSerializer(info)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = customSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        info.delete()
        return response.Response(
            {
                "message": "Information customer service deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
