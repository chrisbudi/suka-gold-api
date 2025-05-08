from re import I
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from user.models import user, users_reset_token
from drf_spectacular.utils import extend_schema, OpenApiParameter
from user.api.serializers import ResetRequestSerializer, ApplyResetSerializer


@extend_schema(
    tags=["User - Reset Password"],
    request=ResetRequestSerializer,
)
class RequestResetView(viewsets.GenericViewSet):
    serializer_class = ResetRequestSerializer

    # @extend_schema(
    #     parameters=[
    #         OpenApiParameter(
    #             name="token",
    #             required=True,
    #             type=str,
    #             description="The token to be used for password reset.",
    #         ),
    #     ]
    # )
    def get(self, request, token):
        # get request pin
        request_token = token
        if request_token:
            # Check if the token is valid
            token_obj = get_object_or_404(
                users_reset_token.user_reset_token, token=request_token
            )
            if token_obj.is_valid():
                return JsonResponse({"message": "Token is valid."})
            else:
                return JsonResponse({"message": "Token is expired."}, status=400)
        else:
            return JsonResponse({"message": "Token is required."}, status=400)

    def post(self, request):
        serializer = ResetRequestSerializer(data=request.data)
        if serializer.is_valid():

            data = dict(serializer.data)
            modelUser = user.objects.get(email=data["email"])
            # Create token
            token = users_reset_token.user_reset_token.objects.create(user=modelUser)

            # Send email
            token.send_reset_email(data.get("type"))
            return JsonResponse({"message": "Password reset email sent."})

        return JsonResponse(serializer.errors, status=400)


@extend_schema(
    tags=["User - Reset Password"],
    request=ApplyResetSerializer,
)
class ResetView(viewsets.GenericViewSet):
    serializer_class = ApplyResetSerializer

    def post(self, request, token):
        serializer = ApplyResetSerializer(data=request.data)
        if serializer.is_valid():
            data = dict(serializer.data)

            token_obj = get_object_or_404(
                users_reset_token.user_reset_token, token=token
            )
            user = token_obj.user

            if data["new_data_type"] == "PIN":
                user.pin = data["new_data"]
            else:
                user.set_password(data["new_data"])

            user.save()

            token_obj.delete()
            token_obj.send_reset_email_done(data.get("new_data_type"))

            return JsonResponse({"message": "Password reset successful."})
        return JsonResponse(serializer.errors, status=400)
