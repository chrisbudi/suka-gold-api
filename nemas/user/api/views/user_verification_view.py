"""
views for the user API
"""

from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.api.serializers import UserKtpSerializer
from nemas.shared_kernel.services.image_services import image_to_base64


@extend_schema(
    tags=["User - User KTP Verify view"],
)
class CreateKtpIfNotVerify(generics.CreateAPIView):
    """Create a new user KTP in the system"""

    authentication_classes = [JWTAuthentication]
    serializer_class = UserKtpSerializer
    permission_classes = [IsAuthenticated]

    def upload_ktp_verify_user(self, serializer):

        # Check if the user is already verified
        serializer.save(create_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)
