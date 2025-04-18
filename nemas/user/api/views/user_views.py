"""
views for the user API
"""

from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
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

        if not id:
            raise ValueError("Phone number is required")

        # Pass the id directly to the method without keyword argument
        user_instance = self.get_user_by_identifier(id)
        user_data = UserSerializer(user_instance).data
        return Response({"user": user_data}, status=200)

    def get_user_by_identifier(self, id: str):
        """Retrieve user profile by phone number"""
        # Query for user by phone number or email
        user_instance = (
            user.objects.filter(phone_number=id).first()
            or user.objects.filter(email=id).first()
        )
        return user_instance
