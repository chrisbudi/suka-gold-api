"""
views for the user API
"""

from rest_framework import generics, permissions
from rest_framework.settings import api_settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from user.api.serializers import UserPropSerializer


@extend_schema(
    tags=["User - User Prop retrieve update"],
)
class UserPropView(generics.RetrieveAPIView):
    """View user prop view in the system"""

    serializer_class = UserPropSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (permissions.IsAuthenticated,)
