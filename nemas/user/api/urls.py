"""
URL mapping for user app
"""

from django.urls import path
from .views import (
    CreateTokenView,
    ManageRefreshTokenView,
    ManageVerifyTokenView,
    CreateUserView,
    ManageUserView,
    CreateUserKtpView,
    CreateUserPropView,
    RetrieveUpdateUserKtpView,
    RetrieveUpdateUserPropView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "user"

user_view_url = []


urlpatterns = [
    path("api/token/", CreateTokenView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", ManageRefreshTokenView.as_view(), name="token_refresh"),
    path("api/token/verify/", ManageVerifyTokenView.as_view(), name="token_verify"),
    path("create/", CreateUserView.as_view(), name="create"),
    # path("token/", CreateTokenView.as_view(), name="token"),
    # path("me/", ManageUserView.as_view(), name="me"),
    path("user_prop/create/", CreateUserPropView.as_view(), name="user_prop_create"),
    path(
        "user_prop/",
        RetrieveUpdateUserPropView.as_view(),
        name="user_prop_retrieve_update",
    ),
    path("user_ktp/create", CreateUserKtpView.as_view(), name="user_ktp_create"),
    path(
        "user_ktp/",
        RetrieveUpdateUserKtpView.as_view(),
        name="user_ktp_retrieve_update",
    ),
]
