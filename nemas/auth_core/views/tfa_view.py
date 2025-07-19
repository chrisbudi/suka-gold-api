from django.contrib.auth import authenticate, get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import qrcode
import base64
from io import BytesIO
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.decorators import action
from rest_framework import viewsets

User = get_user_model()


class tfa_view(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "partial_token": {"type": "string", "description": "User ID"},
                    "otp": {"type": "string", "description": "One-time password"},
                },
                "required": ["partial_token", "otp"],
            }
        },
        responses={
            200: OpenApiExample(
                "Success",
                value={"refresh": "jwt-refresh-token", "access": "jwt-access-token"},
                status_codes=["200"],
            ),
            400: OpenApiExample(
                "Invalid OTP or user",
                value={"detail": "Invalid OTP"},
                status_codes=["400"],
            ),
        },
        description="Verify 2FA OTP and return JWT tokens if valid.",
        tags=["2FA"],
    )
    @action(detail=False, methods=["post"], url_path="verify")
    def verify(self, request):
        user_id = request.data.get("partial_token")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user"}, status=400)

        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if device and device.verify_token(otp):
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )

        return Response({"detail": "Invalid OTP"}, status=400)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiExample(
                "Setup",
                value={
                    "config_url": "otpauth://totp/...",
                    "qr_code_base64": "data:image/png;base64,...",
                },
                status_codes=["200"],
            ),
        },
        description="Setup 2FA and get QR code.",
        tags=["2FA"],
    )
    @action(detail=False, methods=["post"], url_path="setup")
    def setup(self, request):
        user = request.user
        TOTPDevice.objects.filter(user=user, confirmed=False).delete()

        device = TOTPDevice.objects.create(user=user, confirmed=False)
        from urllib.parse import quote

        issuer = quote("nemas.id")
        label = quote(f"nemas.id:{user.email}")
        secret = device.bin_key.hex().upper()
        config_url = f"otpauth://totp/{label}?secret={secret}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
        print(config_url, "config url")
        qr = qrcode.make(config_url)
        buffer = BytesIO()
        qr.save(buffer)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        print(config_url, "config url")
        return Response(
            {
                "config_url": config_url,
                "qr_code_base64": f"data:image/png;base64,{qr_base64}",
            }
        )

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "otp": {"type": "string", "description": "One-time password"},
                },
                "required": ["otp"],
            }
        },
        responses={
            200: OpenApiExample(
                "Confirm",
                value={"detail": "2FA enabled successfully"},
                status_codes=["200"],
            ),
            400: OpenApiExample(
                "Invalid OTP", value={"detail": "Invalid OTP"}, status_codes=["400"]
            ),
        },
        description="Confirm 2FA setup.",
        tags=["2FA"],
    )
    @action(detail=False, methods=["post"], url_path="confirm")
    def confirm(self, request):
        otp = request.data.get("otp")
        device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
        if device and device.verify_token(otp):
            device.confirmed = True
            device.save()
            return Response({"detail": "2FA enabled successfully"})
        return Response({"detail": "Invalid OTP"}, status=400)
