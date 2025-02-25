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
]
