"""
views for the user API
"""

import time
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import (
    status,
    viewsets,
    response,
    views,
    permissions,
)

from drf_spectacular.utils import extend_schema
from user.api.serializers import (
    UserKtpSerializer,
    UploadSerializer,
    UserSerializer,
)
from user.models import user_ktp as modelInfo, user as userModel
from shared_kernel.services import image_services, s3_services
from shared_kernel.services.external import verihub_services


@extend_schema(
    tags=["User - User KTP Verify view"],
)
class CreateKtpIfNotVerify(viewsets.ModelViewSet):
    """Create a new user KTP in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # KTP Verification
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
        if not serializer.is_valid():
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        try:

            user = userModel.objects.get(pk=request.user.id)

            image = image_services.get_file_from_temp(request.user.id)
            s3 = s3_services.S3Service()
            image_s3_url = s3.upload_file(image, f"KTP/{str(request.user.id)}.jpg")
            # Check if the instance exists and update or create it
            instance = modelInfo.objects.update_or_create(
                user=request.user,
                defaults={
                    "updated_user": str(request.user),
                    "create_user": str(request.user),
                },
            )

            serializer = UserKtpSerializer(instance)
            serializer.save()

            userModel.objects.filter(pk=request.user.id).update(
                photo_ktp_url=image_s3_url,
                update_time=time.time(),
                updated_user=str(request.user),
            )

            user.verify_update_state("verify_ktp")
            # image_services.delete_file_from_temp(request.user.id)
            return response.Response(
                {"message": "KTP verified successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            user.verify_update_fail_notes(str(e))
            return response.Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# get user ktp
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
            UserKtpSerializer(user).data,
            status=status.HTTP_200_OK,
        )


# Compare photo and KTP
@extend_schema(
    tags=["User - User Photo Verify view"],
)
class CreateComparePhotoANDKtp(viewsets.ModelViewSet):
    """Create a new user KTP in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=UploadSerializer,
        responses={
            200: {
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

                imageKtp = image_services.get_file_from_temp(request.user.id)
                strImagePhoto = image.image_to_base64(file, request.user.id)
                strImageKtp = image.image_to_base64(imageKtp, request.user.id)
                # image 1 = KTP
                # image 2 = Selfie
                payload = {
                    "image_1": strImageKtp,
                    "image_2": strImagePhoto,
                    "is_liveness": True,
                    "is_quality": True,
                    "is_attribute": True,
                    "threshold": "basic",
                    "validate_quality": False,
                }
                result = verihub.compare_photo_file(payload)
                # get similiarity result
                if result["similarity_status"] == "True":

                    # get data from user ktp
                    user = userModel.objects.get(pk=request.user.id)
                    user.verify_update_state("verify_photo")
                    userKtp = modelInfo.objects.get(user=request.user)

                    payloadKtp = {
                        "nik": userKtp.nik,
                        "name": userKtp.full_name,
                        "birth_date": userKtp.date_of_birth,
                        "email": user.email,
                        "phone": user.phone_number,
                        "selfie_photo": strImagePhoto,
                        "ktp_photo": strImageKtp,
                    }

                    result = verihub.verify_identity(payloadKtp)

                    image_services.delete_file_from_temp(request.user.id)
                    return response.Response(
                        {"message": "result is similarity", "result": result},
                        status=status.HTTP_202_ACCEPTED,
                    )
                else:
                    return response.Response(
                        {"message": "result is not similarity", "result": result},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            except Exception as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
