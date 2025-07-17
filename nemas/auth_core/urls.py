from django.urls import path, include
from auth_core.views import email_otp_views

app_name = "auth_core"

otp_url = [
    path(
        "request-otp/",
        email_otp_views.as_view({"post": "request_otp"}),
        name="request_otp",
    ),
    path(
        "verify-otp/",
        email_otp_views.as_view({"post": "verify_otp"}),
        name="verify_otp",
    ),
]

urlpatterns = [
    path("", include(otp_url), name="otp"),
]
