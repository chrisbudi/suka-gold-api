from core.payment.api.serializers import (
    PaymentMethodSerializer as objectSerializer,
    PaymentMethodFilter as objectFilter,
)
from rest_framework import status, viewsets, filters, pagination, response
from core.domain import payment_method as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from shared.services.s3_services import S3Service
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["payment - method - view"],
)
class PaymentMethodViewViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = objectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = objectFilter
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
        serializer = objectSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = objectSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = objectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, id=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=id)
        serializer = objectSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save(create_user=request.user)
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
                "message": "Payment Method object deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
