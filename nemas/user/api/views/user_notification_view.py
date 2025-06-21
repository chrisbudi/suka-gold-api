from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from rest_framework import status, viewsets, filters, pagination, response
from core.domain import gold_cert_detail_price as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated

from user.api.serializers import (
    UserNotificationSerializer as objectSerializer,
    UserNotificationFilterSerializer as objectFilter,
)


@extend_schema(
    tags=["User - User notification"],
)
class user_notification_views(viewsets.ModelViewSet):
    """View user prop view in the system"""

    queryset = modelInfo.objects.all()
    serializer_class = objectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = (
        pagination.LimitOffsetPagination
    )  # Adjust pagination class as needed

    @extend_schema(
        tags=["User - List User notification"],
    )
    def list(self, request):
        queryset = modelInfo.objects.filter(user_from=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = objectSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
