"""
views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from user.api.serializers import UserSerializer, AuthenticatedTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    """Create a new auth token for user"""

    serializer_class = AuthenticatedTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageRefreshTokenView(TokenRefreshView):
    """Implement refresh token"""

    serializer_class = AuthenticatedTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageVerifyTokenView(TokenVerifyView):
    """Implement verify token"""

    serializer_class = AuthenticatedTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        print(self.request)
        return self.request.user
