from django.urls import path, include
from auth_core.views import otp_view, tfa_view
from auth_core.views.tfa_view import tfa_view

app_name = "auth_core"

otp_url = [
    path(
        "request-otp/",
        otp_view.email_otp_views.as_view({"post": "request_otp"}),
        name="request_otp",
    ),
    path(
        "verify-otp/",
        otp_view.email_otp_views.as_view({"post": "verify_otp"}),
        name="verify_otp",
    ),
    path("api/verify-2fa/", tfa_view.as_view({"post": "verify"}), name="verify_tfa"),
    path("api/setup-2fa/", tfa_view.as_view({"post": "setup"}), name="setup_2fa"),
    path("api/confirm-2fa/", tfa_view.as_view({"post": "confirm"}), name="confirm_2fa"),
]

urlpatterns = [
    path("", include(otp_url), name="otp"),
]
