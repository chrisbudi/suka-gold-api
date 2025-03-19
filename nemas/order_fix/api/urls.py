"""
URL mapping for cart app
"""

from django.urls import path
from order_fix.api import views
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
                    "show",
                    views.CartItemListAPIView.as_view({"get": "show_cart"}),
                    name="show_cart",
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
            ]
        ),
    ),
    path(
        "shipping/service/",
        views.OrderShippingAPIView.as_view({"post": "list_shipping_service"}),
        name="shipping-service",
    ),
]
