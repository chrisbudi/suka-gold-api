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
)


app_name = "user"

user_view_url = []


urlpatterns = [
    path("token/", CreateTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", ManageRefreshTokenView.as_view(), name="token_refresh"),
    path("token/verify/", ManageVerifyTokenView.as_view(), name="token_verify"),
    path("create/", CreateUserView.as_view(), name="create"),
    path("create/super_user/", CreateSuperUserView.as_view(), name="create_super_user"),
    # path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="me"),
    # path(
    #     "user_prop/create/",
    #     CreateUserPropView.as_view(),
    #     name="user_prop_create",
    # ),
    path(
        "user_prop/",
        UserPropView.as_view(),
        name="user_prop_retrieve",
    ),
    # path("user_ktp/create", CreateUserKtpView.as_view(), name="user_ktp_create"),
    # path(
    #     "user_ktp/",
    #     RetrieveUpdateUserKtpView.as_view(),
    #     name="user_ktp_retrieve_update",
    # ),
]
