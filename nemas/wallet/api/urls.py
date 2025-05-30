"""
URL mapping for wallet app
"""

from django.urls import path
from .views import TopupTransactionView, SimulatePaymentViews, DisburstmentViews
from .webhook import qris_webhook_view, va_webhook_view

app_name = "wallet"

wallet_view_url = []


urlpatterns = [
    path(
        "topup/va/",
        TopupTransactionView.as_view({"post": "generate_va"}),
        name="topup_va",
    ),
    path(
        "topup/qris/",
        TopupTransactionView.as_view({"post": "generate_qris"}),
        name="topup_qris",
    ),
    path(
        "simulate/payment/qris/",
        SimulatePaymentViews.SimulatePaymentView.as_view(
            {"post": "simulate_payment_qris"}
        ),
        name="simulate_payment_qris",
    ),
    path(
        "simulate/payment/va/",
        SimulatePaymentViews.SimulatePaymentView.as_view(
            {"post": "simulate_payment_va"}
        ),
        name="simulate_payment_va",
    ),
    path("webhooks/qris/", qris_webhook_view, name="qris_webhook"),
    path("webhooks/va/", va_webhook_view, name="va_webhook"),
    path(
        "disburst/",
        DisburstmentViews.DisburstTransactionView.as_view({"post": "generate"}),
        name="disburst",
    ),
]
