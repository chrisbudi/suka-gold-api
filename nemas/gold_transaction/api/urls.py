"""
URL mapping for wallet app
"""

from django.urls import path
from gold_transaction.api import views

app_name = "wallet"


wallet_view_url = []


urlpatterns = [
    path(
        "gold-purchases/",
        views.GoldPurchaseListCreateAPIView.as_view({"get": "list"}),
        name="gold-purchase-list",
    ),
    path(
        "gold-purchases/create",
        views.GoldPurchaseListCreateAPIView.as_view({"post": "perform_create"}),
        name="gold-purchase-create",
    ),
    path(
        "gold-sales/",
        views.GoldSaleListCreateAPIView.as_view({"get": "list"}),
        name="gold-sale-list",
    ),
    path(
        "gold-sales/create",
        views.GoldSaleListCreateAPIView.as_view({"post": "perform_create"}),
        name="gold-sale-create",
    ),
    path(
        "gold-transfer/",
        views.GoldTransferListCreateAPIView.as_view({"get": "list"}),
        name="gold-sale-list",
    ),
    path(
        "gold-transfer/calculate",
        views.GoldTransferListCreateAPIView.as_view({"post": "calculate_weight"}),
        name="gold-sale-list",
    ),
    path(
        "gold-transfer/create",
        views.GoldTransferListCreateAPIView.as_view({"post": "perform_create"}),
        name="gold-sale-create",
    ),
    # path(
    #     "gold-purchases/<str:pk>/",
    #     views.GoldPurchaseRetrieveUpdateDestroyAPIView.as_view(),
    #     name="gold-purchase-detail",
    # ),
]
