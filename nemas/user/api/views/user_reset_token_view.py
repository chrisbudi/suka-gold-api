from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from user.models import user, users_reset_token
from drf_spectacular.utils import extend_schema
from user.api.serializers import EmailSerializer, ResetPasswordSerializer


@extend_schema(
    tags=["User - Reset Password"],
    request=EmailSerializer,
    responses={200: "Password reset email sent.", 404: "User not found."},
)
class RequestPasswordResetView(viewsets.GenericViewSet):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        print(serializer, "serializer")
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        email = serializer.data["email"]  # type: ignore
        print(email, "email")
        modelUser = user.objects.get(email=email)
        print(email, modelUser, "email and modelUser")
        # Create token
        token = users_reset_token.user_reset_token.objects.create(user=modelUser)

        # Send email
        token.send_reset_password_email(request)
        return JsonResponse({"message": "Password reset email sent."})


@extend_schema(
    tags=["User - Reset Password"],
)
class ResetPasswordView(viewsets.GenericViewSet):
    serializer_class = ResetPasswordSerializer

    def post(self, request, token):
        serializer = ResetPasswordSerializer(data=request.data)
        print(serializer, "serializer")
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_password = serializer.data["new_password"]  # type: ignore

        token_obj = get_object_or_404(users_reset_token.user_reset_token, token=token)
        user = token_obj.user

        user.set_password(new_password)
        user.save()

        token_obj.delete()

        token_obj.send_reset_password_email_done()

        return JsonResponse({"message": "Password reset successful."})
