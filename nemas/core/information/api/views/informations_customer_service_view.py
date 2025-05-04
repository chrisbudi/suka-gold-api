from core.information.api.serializers import (
    InformationCustomerServiceSerializer as infoSerializer,
    InformationCustomerServiceFilter as customerFilter,
)
from rest_framework import status, viewsets, filters, pagination, response


from core.domain import information_customer_service as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["Information - Customer Service"],
)
class InformationCustomerServiceViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = customerFilter
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed
    ordering_fields = ["id", "create_time", "upd_time"]
    ordering = ["-create_time"]

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = modelInfo.objects.all()
        queryset = self.filter_queryset(queryset)

        # implement ordering
        ordering_filter = filters.OrderingFilter()
        queryset = ordering_filter.filter_queryset(request, queryset, self)

        # implement pagination
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = infoSerializer(info)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = infoSerializer(
            info, data=request.data, context={"request": request}
        )
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
