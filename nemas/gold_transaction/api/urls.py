"""
URL mapping for ewallet app
"""

from django.urls import path
from gold_transaction.api import views

app_name = "ewallet"


ewallet_view_url = []


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
    # path(
    #     "gold-purchases/<str:pk>/",
    #     views.GoldPurchaseRetrieveUpdateDestroyAPIView.as_view(),
    #     name="gold-purchase-detail",
    # ),
]
