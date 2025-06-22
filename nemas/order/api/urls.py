"""
URL mapping for cart app
"""

from django.urls import path
from order.api import views
from django.urls import include

app_name = "order-fix"


urlpatterns = [
    path(
        "cart/",
        include(
            [
                path(
                    "detail/",
                    views.CartItemListAPIView.as_view({"get": "list_cart_detail"}),
                    name="list-cart-detail",
                ),
                path(
                    "add/",
                    views.CartItemListAPIView.as_view({"post": "add_cart"}),
                    name="cart-add",
                ),
                path(
                    "process/",
                    views.CartItemListAPIView.as_view({"post": "process_cart"}),
                    name="cart-add",
                ),
                path(
                    "delete/<uuid:pk>/",
                    views.CartItemListAPIView.as_view({"delete": "destroy"}),
                    name="cart-delete",
                ),
            ],
        ),
    ),
    path(
        "shipping/service/",
        views.OrderShippingServiceAPIView.as_view({"post": "list_shipping_service"}),
        name="shipping-service",
    ),
    path(
        "order/",
        include(
            [
                path(
                    "list/",
                    views.OrderGoldAPIView.as_view({"get": "list"}),
                    name="list-order",
                ),
                path(
                    "create/",
                    views.OrderGoldAPIView.as_view({"post": "perform_create"}),
                    name="order-create",
                ),
            ],
        ),
    ),
    path(
        "order/payment/",
        include(
            [
                path(
                    "simulate/va/",
                    views.OrderPaymentView.as_view({"post": "simulate_va_payment"}),
                    name="order-va-payment",
                ),
                path(
                    "simulate/qris/",
                    views.OrderPaymentView.as_view({"post": "simulate_qris_payment"}),
                    name="order-qris-payment",
                ),
            ],
        ),
    ),
]
