# views.py
import random
from django.contrib.auth import get_user_model
from auth_core.models import email_otp
from drf_spectacular.utils import extend_schema

from shared.services.email_service import EmailService

from django.template.loader import render_to_string

from rest_framework import status, viewsets, filters, pagination, response, permissions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()


class email_otp_views(viewsets.ModelViewSet):

    @extend_schema(
        tags=["OTP Authentication"],
        description="Handles email OTP requests and verifications.",
        methods=["POST"],
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                },
                "required": ["email"],
            }
        },
        responses={
            status.HTTP_200_OK: "OTP sent successfully.",
            status.HTTP_400_BAD_REQUEST: "Invalid request data.",
            status.HTTP_404_NOT_FOUND: "Email not found.",
        },
    )
    def request_otp(self, request):
        if request.method == "POST":
            email = request.data.get("email")
            if not email:
                return response.Response(
                    {"error": "Email is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # check if email exists in the database
            if not User.objects.filter(email=email).exists():
                return response.Response(
                    {"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND
                )

            code = str(random.randint(100000, 999999))

            email_otp.objects.create(email=email, code=code)
            # Send email using SendGrid

            sendGridEmail = settings.SENDGRID_EMAIL

            mail = Mail(
                from_email=sendGridEmail["DEFAULT_FROM_EMAIL"],
                to_emails=[email],
                subject="Nemas OTP Code",
                plain_text_content=f"Your OTP code is: {code}. Please use this code to verify your email.",
            )

            try:
                mailService = EmailService()
                mailService.sendMail(mail)

            except Exception as e:
                return response.Response(
                    {"error": "Failed to send email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return response.Response(
                {"message": "OTP sent successfully"}, status=status.HTTP_200_OK
            )

    @extend_schema(
        tags=["OTP Authentication"],
        description="Handles email OTP requests and verifications.",
        methods=["POST"],
        responses={
            status.HTTP_200_OK: "OTP sent successfully.",
            status.HTTP_400_BAD_REQUEST: "Invalid request data.",
            status.HTTP_404_NOT_FOUND: "Email not found.",
        },
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "code": {
                        "type": "string",
                        "minLength": 6,
                        "maxLength": 6,
                        "required": True,
                    },
                },
                "required": ["email"],
            }
        },
    )
    def verify_otp(self, request):
        if request.method == "POST":
            email = request.data.get("email")
            code = request.data.get("code")

            otp = (
                email_otp.objects.filter(email=email, code=code)
                .order_by("-created_at")
                .first()
            )
            if otp and not otp.is_expired():
                user, _ = User.objects.get_or_create(
                    email=email, defaults={"username": email}
                )
                refresh = RefreshToken.for_user(user)
                return response.Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return response.Response(
                    {"error": "Invalid or expired code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return response.Response(
            {"error": "Invalid request method."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
