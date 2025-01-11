"""
URL mapping for user app
"""

from django.urls import path
from .views import (
    CreateTokenView,
    ManageRefreshTokenView,
    ManageVerifyTokenView,
    CreateUserView,
    CreateSuperUserView,
    ManageUserView,
    # user props
    UserPropView,
    UserKtpView,
    UserPinView,
    CreateKtpIfNotVerify,
    ResetPasswordView,
    RequestPasswordResetView,
)


app_name = "user"

user_view_url = []


urlpatterns = [
    path(
        "token/request-reset-password",
        view=RequestPasswordResetView.as_view({"post": "post"}),
        name="token_reset_password",
    ),
    path(
        "token/reset-password/<str:token>/",
        view=ResetPasswordView.as_view({"post": "post"}),
        name="token_reset_password_done",
    ),
    path("token/", CreateTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", ManageRefreshTokenView.as_view(), name="token_refresh"),
    path("token/verify/", ManageVerifyTokenView.as_view(), name="token_verify"),
    path("create/", CreateUserView.as_view(), name="create"),
    path("create/super_user/", CreateSuperUserView.as_view(), name="create_super_user"),
    path("me/", ManageUserView.as_view(), name="me"),
    # path(
    #     "user_prop/create/",
    #     CreateUserPropView.as_view(),
    #     name="user_prop_create",
    # ),
    path(
        "user/prop/",
        UserPropView.as_view(),
        name="user_prop_retrieve",
    ),
    path(
        "user/ktp/",
        UserKtpView.as_view(),
        name="user_ktp_retrieve",
    ),
    path(
        "user/ktp/verify/",
        CreateKtpIfNotVerify.as_view({"post": "upload_ktp_verify_user"}),
        name="user_ktp_verify",
    ),
    path(
        "user/ktp/verify/approve",
        CreateKtpIfNotVerify.as_view({"post": "submit_verify"}),
        name="user_ktp_verify_approve",
    ),
    path(
        "user/pin/submit/", UserPinView.as_view({"post": "post"}), name="user-pin-post"
    ),
    path("user/pin/get/", UserPinView.as_view({"get": "get"}), name="user-pin-get"),
    path(
        "user/pin/verify/",
        UserPinView.as_view({"post": "verify"}),
        name="user-pin-verify",
    ),
    # path(
    #     "user_ktp/",
    #     RetrieveUpdateUserKtpView.as_view(),
    #     name="user_ktp_retrieve_update",
    # ),
]
