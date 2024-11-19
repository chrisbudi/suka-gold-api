from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from user.api.serializers import UserKtpSerializer
from nemas.user.models.users import user_ktp


@extend_schema(
    tags=["User - User ktp create"],
)
class CreateUserKtpView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserKtpSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)


@extend_schema(
    tags=["User - User ktp retrieve update"],
)
class UserKtpView(generics.RetrieveAPIView):
    """Create a new user in the system"""

    serializer_class = UserKtpSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
