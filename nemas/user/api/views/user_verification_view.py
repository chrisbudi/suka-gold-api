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
from shared_kernel.services import image_services, s3_services, verihub_services


@extend_schema(
    tags=["User - User KTP Verify view"],
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
    def upload_ktp_verify_user(self, request):
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

    @extend_schema(
        request=UserKtpSerializer,
        responses={
            201: {"type": "object", "properties": {"message": {"type": "string"}}}
        },
        tags=["User - KTP Verification"],
    )
    def submit_verify(self, request):
        serializer = UserKtpSerializer(data=request.data)
        try:

            if serializer.is_valid():
                image = image_services.get_file_from_temp(request.user.id)
                s3 = s3_services.S3Service()
                imageS3 = s3.upload_file(image, f"KTP/{str(request.user.id)}.jpg")
                instance = modelInfo.objects.filter(user=self.request.user).first()
                if instance:
                    instance.photo_url = imageS3
                    instance.updated_user = str(self.request.user)
                    instance.save()
                else:
                    instance = modelInfo.objects.create(
                        user=self.request.user,
                        create_user=str(self.request.user),
                        photo_url=imageS3,
                    )
                serializer = UserKtpSerializer(instance)
                image_services.delete_file_from_temp(request.user.id)
                return response.Response(
                    {"message": "KTP verified successfully"},
                    status=status.HTTP_201_CREATED,
                )

            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["User - User ktp retrieve"],
)
class UserKtpView(views.APIView):
    """Create a new user in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Retrieve and return authenticated user"""
        try:
            user = modelInfo.objects.get(user=request.user)
        except modelInfo.DoesNotExist:
            return response.Response({"detail": "User KTP not found."}, status=404)

        user_ktp_data = dict(UserKtpSerializer(user).data)
        return response.Response(
            {
                **user_ktp_data,
            },
            status=200,
        )
