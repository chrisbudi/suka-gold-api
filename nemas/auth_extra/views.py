# views.py
import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, login
from auth_extra.models import EmailOTP
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from rest_framework import status, viewsets, filters, pagination, response, permissions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class email_otp_views(viewsets.ModelViewSet):

    @extend_schema(
        tags=["OTP Authentication"],
        description="Handles email OTP requests and verifications.",
        methods=["POST"],
        responses={
            status.HTTP_200_OK: "OTP sent successfully.",
            status.HTTP_400_BAD_REQUEST: "Invalid request data.",
            status.HTTP_404_NOT_FOUND: "Email not found.",
        },
        parameters=[
            OpenApiParameter(
                name="email",
                description="Email address for OTP",
                required=True,
                type=str,
            ),
        ],
    )
    def request_otp(self, request):
        if request.method == "POST":
            email = request.POST["email"]
            # check if email exists in the database
            if not User.objects.filter(email=email).exists():
                return response.Response(
                    {"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND
                )

            code = str(random.randint(100000, 999999))

            EmailOTP.objects.create(email=email, code=code)
            # Send email using SendGrid

            message = Mail(
                from_email="noreply@example.com",
                to_emails=email,
                subject="Your Login Code",
                plain_text_content=f"Your OTP is {code}",
            )
            try:
                sg = SendGridAPIClient("YOUR_SENDGRID_API_KEY")
                sg.send(message)
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
        parameters=[
            OpenApiParameter(
                name="email",
                description="Email address for OTP",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="code",
                description="OTP code to verify",
                required=True,
                type=str,
            ),
        ],
    )
    def verify_otp(self, request):
        if request.method == "POST":
            email = request.POST["email"]
            code = request.POST["code"]

            otp = (
                EmailOTP.objects.filter(email=email, code=code)
                .order_by("-created_at")
                .first()
            )
            if otp and not otp.is_expired():
                user, _ = User.objects.get_or_create(
                    email=email, defaults={"username": email}
                )
                refresh = RefreshToken.for_user(user)
                return {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            else:
                return response.Response(
                    {"error": "Invalid or expired code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return response.Response(
            {"error": "Invalid request method."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
