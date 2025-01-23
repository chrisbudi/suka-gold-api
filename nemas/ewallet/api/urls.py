"""
URL mapping for ewallet app
"""

from django.urls import path
from .views import TopupTransactionView

app_name = "ewallet"

ewallet_view_url = []


urlpatterns = [
    path(
        "topup/va/",
        TopupTransactionView.as_view({"post": "generate_va"}),
        name="topup_va",
    ),
    path(
        "topup/va/simulate/",
        TopupTransactionView.as_view({"post": "simulate_payment_va"}),
        name="topup_simulate_payment_va",
    ),
    path(
        "topup/qris/",
        TopupTransactionView.as_view({"post": "generate_qris"}),
        name="topup_qris",
    ),
    path(
        "topup/qris/simulate/",
        TopupTransactionView.as_view({"post": "simulate_payment_qris"}),
        name="topup_simulate_payment_qris",
    ),
]
