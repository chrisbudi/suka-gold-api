"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    admin_fee_view as views_admin_fee,
)

router = DefaultRouter()

app_name = "admin_fee"
# customer service


# promo
admin_fee_url = [
    path(
        "",
        views_admin_fee.AdminFeeViewSet.as_view({"get": "list"}),
        name="list_article",
    ),
    path(
        "create/",
        views_admin_fee.AdminFeeViewSet.as_view({"post": "create"}),
        name="post_article",
    ),
    path(
        "<int:id>/",
        views_admin_fee.AdminFeeViewSet.as_view({"patch": "update"}),
        name="patch_article",
    ),
    path(
        "<int:id>/",
        views_admin_fee.AdminFeeViewSet.as_view({"delete": "destroy"}),
        name="delete_article",
    ),
    path(
        "get/<int:id>/",
        views_admin_fee.AdminFeeViewSet.as_view({"get": "retrieve"}),
        name="get_article",
    ),
]

urlpatterns = [
    path("fee/", include(admin_fee_url)),
]
