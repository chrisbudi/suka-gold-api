"""
URL mapping for cart app
"""

from django.urls import path
from order_fix.api import views

app_name = "order-fix"


urlpatterns = [
    path(
        "cart/detail/",
        views.CartItemListAPIView.as_view({"get": "list_cart_detail"}),
        name="list-cart-detail",
    ),
    path(
        "cart/show",
        views.CartItemListAPIView.as_view({"get": "show_cart"}),
        name="show_cart",
    ),
    path(
        "cart/add/",
        views.CartItemListAPIView.as_view({"post": "add_cart"}),
        name="cart-add",
    ),
    path(
        "cart/delete/<uuid:pk>/",
        views.CartItemListAPIView.as_view({"delete": "destroy"}),
        name="cart-delete",
    ),
]
