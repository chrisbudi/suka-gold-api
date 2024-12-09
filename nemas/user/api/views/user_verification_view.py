"""
views for the user API
"""

from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.api.serializers import UserPropSerializer, UserKtpSerializer


@extend_schema(
    tags=["User - User Verify view"],
)
class CreateUserPropView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserPropSerializer

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)
