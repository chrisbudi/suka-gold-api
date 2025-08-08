"""
views for the user API
"""

from urllib import response
import uuid
from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from user.api.serializers.user_admin_serializer import (
    UserAdminSerializer,
    UserAdminServiceFilter,
)
from django_filters.rest_framework import DjangoFilterBackend
from user.models import user  # Import the User model

from rest_framework import status, viewsets, filters, pagination, permissions


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
            permission_classes = [permissions.IsAuthenticated]
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
        id = kwargs.get("id")
        print(id, "id from kwargs")
        if not id:
            raise ValueError("Phone number is required")

        # Pass the id directly to the method without keyword argument
        user_instance = user.objects.select_related(
            "user_props", "user_ktp", "user_address"
        ).get(pk=id)
        # print(user_instance, "user instance")
        user_data = UserAdminSerializer(user_instance).data
        print(user_data, "user data")
        return Response({"user": user_data}, status=200)

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
        info.is_deleted = True
        info.save(update_fields=["is_deleted"])

        return Response(
            {
                "message": "User object deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
