"""
views for the user API
"""

import uuid
from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, pagination
from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.authentication import JWTAuthentication


from user.api.serializers import UserSerializer, AuthTokenObtainPairSerializer
from user.models import user  # Import the User model


@extend_schema(
    tags=["User - User Manager"],
)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


@extend_schema(
    tags=["User - User Manager"],
)
class CreateSuperUserView(generics.CreateAPIView):
    """Create a new superuser in the system"""

    serializer_class = UserSerializer

    def get_serializer_context(self):
        """Add context to the serializer"""
        context = super().get_serializer_context()
        context["is_superuser"] = True
        return context


@extend_schema(
    tags=["User - Token User Manager"],
)
class CreateTokenView(TokenObtainPairView):
    """Create a new auth token for user"""

    serializer_class = AuthTokenObtainPairSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(
    tags=["User - Token User Manager"],
)
class ManageRefreshTokenView(TokenRefreshView):
    """Implement refresh token"""

    serializer_class = AuthTokenObtainPairSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(
    tags=["User - Token User Manager"],
)
class ManageVerifyTokenView(TokenVerifyView):
    """Implement verify token"""

    serializer_class = AuthTokenObtainPairSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(
    tags=["User - User Manager"],
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    # update password
    def update(self, request, *args, **kwargs):
        """Update the authenticated user"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(
    tags=["User - Admin"],
)
class UserAdminView(viewsets.ModelViewSet):
    """List all users or retrieve a single user by ID"""

    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        """List users with pagination and support for page/page_size query params"""
        queryset = user.objects.select_related("user_props").all()
        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get(self, request, *args, **kwargs):
        """Retrieve a single user by ID"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@extend_schema(
    tags=["User - get by phone number"],
)
class GETUserProfileByPhoneNumberView(viewsets.ModelViewSet):
    """Retrieve user profile by phone number"""

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # The 'id' is passed as part of the URL, so you can access it through kwargs
        id = kwargs.get("id")
        print(id, "id from kwargs")
        if not id:
            raise ValueError("Phone number is required")

        # Pass the id directly to the method without keyword argument
        user_instance = self.get_user_by_identifier(id)
        # print(user_instance, "user instance")
        user_data = UserSerializer(user_instance).data
        print(user_data, "user data")
        return Response({"user": user_data}, status=200)

    def get_user_by_identifier(self, id: uuid.UUID | str):
        """Retrieve user profile by phone number"""
        # Ensure id is a string for filtering
        identifier = str(id)
        user_instance = (
            user.objects.filter(phone_number=identifier).first()
            or user.objects.filter(email=identifier).first()
        )
        return user_instance
