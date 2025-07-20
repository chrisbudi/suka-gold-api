"""
views for the user API
"""

from urllib import response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, pagination, filters, status
from rest_framework.response import Response

from user.api.serializers.user_admin_serializer import (
    UserAdminSerializer,
    UserAdminServiceFilter,
)
from django_filters.rest_framework import DjangoFilterBackend
from user.models import user  # Import the User model
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=["User - Admin"],
)
class UserAdminView(viewsets.ModelViewSet):
    """List all users or retrieve a single user by ID"""

    queryset = user.objects.all()
    serializer_class = UserAdminSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UserAdminServiceFilter

    def get_permissions(self):
        print(self.action, "action permission")
        if self.action in ["list", "get"]:
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """List users with pagination and support for page/page_size query params"""
        queryset = user.objects.all()
        # If "user_props", "user_ktp", and "user_address" are valid relations, use select_related as below:
        queryset = user.objects.select_related(
            "user_props", "user_ktp", "user_address"
        ).all()
        filter_queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(filter_queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, *args, **kwargs):
        """Retrieve a single user by ID"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, id=None):
        info = get_object_or_404(user, pk=id)
        serializer = UserAdminSerializer(
            info, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        queryset = user.objects.all()
        info = get_object_or_404(queryset, pk=id)
        info.delete()
        return Response(
            {
                "message": "Gold object deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
