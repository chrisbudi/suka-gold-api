"""
URL mapping for cart app
"""

from django.urls import path
from order.api import views

app_name = "order"


wallet_view_url = []


urlpatterns = [
    path(
        "cart/",
        views.CartItemListAPIView.as_view({"get": "list"}),
        name="cart-list",
    ),
    path(
        "cart/add/",
        views.CartItemListAPIView.as_view({"post": "perform_create"}),
        name="cart-add",
    ),
    path(
        "cart/update/<uuid:pk>/",
        views.CartItemListAPIView.as_view({"put": "update"}),
        name="cart-update",
    ),
    path(
        "cart/delete/<uuid:pk>/",
        views.CartItemListAPIView.as_view({"delete": "destroy"}),
        name="cart-delete",
    ),
    path(
        "shipping/service/",
        views.OrderShippingAPIView.as_view({"post": "list_shipping_service"}),
        name="shipping-service",
    ),
    path(
        "order/create",
        views.OrderGoldListCreateAPIView.as_view({"post": "perform_create"}),
        name="order-create",
    ),
    path(
        "order/list",
        views.OrderGoldListCreateAPIView.as_view({"get": "list"}),
        name="order-list",
    ),
    path(
        "order/simulate/va/<str:pk>",
        views.OrderGoldListCreateAPIView.as_view({"post": "simulate_va_payment"}),
        name="order-va-payment",
    ),
    path(
        "order/simulate/qris/<str:pk>",
        views.OrderGoldListCreateAPIView.as_view({"post": "simulate_qris_payment"}),
        name="order-qris-payment",
    ),
]
