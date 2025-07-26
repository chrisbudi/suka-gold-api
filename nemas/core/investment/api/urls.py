"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
import investment
from rest_framework.routers import DefaultRouter

from .views import (
    investment_return_viewset,
)

router = DefaultRouter()

app_name = "investment"
# customer service


# promo
investment_return_url = [
    path(
        "",
        investment_return_viewset.as_view({"get": "list"}),
        name="list_article",
    ),
    path(
        "create/",
        investment_return_viewset.as_view({"post": "create"}),
        name="post_article",
    ),
    path(
        "<int:id>/",
        investment_return_viewset.as_view({"patch": "update"}),
        name="patch_article",
    ),
    path(
        "<int:id>/",
        investment_return_viewset.as_view({"delete": "destroy"}),
        name="delete_article",
    ),
    path(
        "get/<int:id>/",
        investment_return_viewset.as_view({"get": "retrieve"}),
        name="get_article",
    ),
]

urlpatterns = [
    path("return/", include(investment_return_url)),
]
