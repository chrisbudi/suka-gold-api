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
]
