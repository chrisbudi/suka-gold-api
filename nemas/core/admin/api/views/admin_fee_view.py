from core.admin.api.serializers import (
    AdminFeeSerializer as infoSerializer,
    AdminFeeFilter as promoFilter,
)

from rest_framework import status, viewsets, filters, pagination, response, permissions
from core.domain import AdminFee as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["invenstment - admin fee"],
)
class AdminFeeViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = promoFilter
    ordering_fields = ["promo_id", "create_time", "upd_time"]
    ordering = ["-create_time"]

    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get", "list_show"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                location="query",
                description="Limit the number of results",
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                location="query",
                description="Offset the results by a certain number",
            ),
            OpenApiParameter(
                name="search", type=str, location="query", description="Search term"
            ),
        ]
    )
    def list(self, request):
        queryset = modelInfo.objects.all()
        queryset = self.filter_queryset(queryset)

        # implement ordering
        ordering_filter = filters.OrderingFilter()
        queryset = ordering_filter.filter_queryset(request, queryset, self)

        paginated_queryset = self.paginate_queryset(queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                location="query",
                description="Limit the number of results",
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                location="query",
                description="Offset the results by a certain number",
            ),
            OpenApiParameter(
                name="search", type=str, location="query", description="Search term"
            ),
        ]
    )
    def list_show(self, request):
        queryset = modelInfo.objects.filter(show_banner=True)
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

    def create(self, request):
        serializer = infoSerializer(data=request.data, context={"request": request})
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
                "message": "Information Promo deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
