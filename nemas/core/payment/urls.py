"""
Url mapping for the recipe app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.views import (
    bank_view,
)

router = DefaultRouter()

app_name = "payment"


bank_urls = [
    path(
        "",
        bank_view.BankServiceViewSet.as_view({"get": "list"}),
        name="list_bank",
    ),
    path(
        "create",
        bank_view.BankServiceViewSet.as_view({"post": "create"}),
        name="create_bank",
    ),
    path(
        "<str:id>/",
        bank_view.BankServiceViewSet.as_view({"patch": "update"}),
        name="patch_bank",
    ),
    path(
        "<str:id>/",
        bank_view.BankServiceViewSet.as_view({"delete": "destroy"}),
        name="delete_bank",
    ),
    path(
        "<str:id>/",
        bank_view.BankServiceViewSet.as_view({"get": "retrieve"}),
        name="get_bank",
    ),
]

urlpatterns = [
    path("bank/", include(bank_urls)),
]
