"""
URL mapping for wallet app
"""

from django.urls import path
from investment.api import views

app_name = "investment"


wallet_view_url = []


urlpatterns = [
    path(
        "transaction/",
        views.TransactionServiceViewSet.as_view({"get": "list"}),
        name="investment-list",
    ),
    path(
        "transaction/create",
        views.TransactionServiceViewSet.as_view({"post": "perform_create"}),
        name="investment-create",
    ),
]
