"""
views for the user API
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import (
    status,
    viewsets,
    response,
    views,
    permissions,
)

from drf_spectacular.utils import extend_schema
from user.api.serializers import UserKtpSerializer, UploadSerializer
from user.models import user_ktp as modelInfo
from shared_kernel.services import image_services, s3_services
from shared_kernel.services.external import verihub_services


@extend_schema(
    tags=["User - User Photo Verify view"],
)
class CreateKtpIfNotVerify(viewsets.ModelViewSet):
    """Create a new user KTP in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UploadSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "url": {"type": "string"},
                },
            }
        },
        tags=["User - KTP Verification"],
    )
    def upload_photo_verify_user(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            if (
                isinstance(serializer.validated_data, dict)
                and "file" in serializer.validated_data
            ):
                file = serializer.validated_data["file"]
            else:
                return response.Response(
                    {"error": "File not provided"}, status=status.HTTP_400_BAD_REQUEST
                )

            verihub = verihub_services.VerihubService()
            image = image_services
            try:
                strImage = image.image_to_base64(file, request.user.id)

                # image 1 = KTP
                # image 2 = Selfie
                payload = {"image": strImage, "validate_quality": False}
                result = verihub.verify_ktp_file(payload)

                return response.Response(
                    {"message": "File uploaded successfully", "result": result},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
