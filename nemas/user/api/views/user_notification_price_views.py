from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from rest_framework import status, viewsets, filters, pagination, response

from user.models import user_notification_price as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated

from user.api.serializers import (
    UserNotificationPriceSerializer as objectSerializer,
)


@extend_schema(
    tags=["User - User notification price"],
)
class user_notification_price_views(viewsets.ModelViewSet):
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
        tags=["User - User notification price"],
        description="Get user notification price settings",
        responses={200: objectSerializer, 404: "Not Found"},
    )
    def get(self, request):
        queryset = get_object_or_404(modelInfo, user=request.user)
        if not queryset:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = objectSerializer(queryset, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=[f"User - User notification price"],
        description="Update user notification price settings",
        request=objectSerializer,
    )
    def post(self, request):
        notification_price, _ = modelInfo.objects.get_or_create(user=request.user)
        serializer = objectSerializer(
            notification_price,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
