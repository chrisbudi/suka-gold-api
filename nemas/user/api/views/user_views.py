"""
views for the user API
"""

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.settings import api_settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.authentication import JWTAuthentication


from user.api.serializers import UserSerializer, AuthTokenObtainPairSerializer


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
