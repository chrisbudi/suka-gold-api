from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from rest_framework import status, viewsets, filters, pagination, response
from user.models import user_notification as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated

from user.api.serializers import (
    UserNotificationSerializer as objectSerializer,
)


@extend_schema(
    tags=["User - User notification"],
)
class user_notification_views(viewsets.ModelViewSet):
    """View user prop view in the system"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
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
        queryset = modelInfo.objects.filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = objectSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
