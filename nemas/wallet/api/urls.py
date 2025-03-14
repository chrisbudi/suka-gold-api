"""
URL mapping for wallet app
"""

from django.urls import path
from .views import TopupTransactionView, SimulatePaymentViews, DisburstmentViews
from .webhook import TopupQrisWebhookViews

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
    path(
        "webhook/qris/",
        TopupQrisWebhookViews.TopupQrisWebhookView.as_view({"post": "post"}),
        name="webhook_qris",
    ),
    path(
        "disburst/",
        DisburstmentViews.DisburstTransactionView.as_view({"post": "generate"}),
        name="disburst",
    ),
]
