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
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(user, "user")
        return self.serializer_class.Meta.model.objects.filter(user_id=user)
