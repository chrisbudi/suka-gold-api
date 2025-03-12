"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .api.views import (
    cert_view,
    gold_cert_price_view,
    gold_view,
    gold_price_config_view,
    gold_price_view,
    gold_promo_view,
)

router = DefaultRouter()

app_name = "gold"
# customer service
gold_urls = [
    path("", gold_view.GoldServiceViewSet.as_view({"get": "list"}), name="list_gold"),
    path(
        "create",
        gold_view.GoldServiceViewSet.as_view({"post": "create"}),
        name="post_gold",
    ),
    path(
        "<int:id>/",
        gold_view.GoldServiceViewSet.as_view({"patch": "update"}),
        name="patch_gold",
    ),
    path(
        "<int:id>/",
        gold_view.GoldServiceViewSet.as_view({"delete": "destroy"}),
        name="delete_gold",
    ),
    path(
        "<int:id>/",
        gold_view.GoldServiceViewSet.as_view({"get": "retrieve"}),
        name="get_gold",
    ),
    path(
        "upload/<int:id>/",
        gold_view.GoldServiceViewSet.as_view({"post": "upload"}),
        name="upload_image_promo",
    ),
]

gold_cert_price_url = [
    path(
        "",
        gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({"get": "list"}),
        name="list_gold_cert_price_config",
    ),
    path(
        "create",
        gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({"post": "create"}),
        name="create_gold_cert_price_config",
    ),
    path(
        "<int:id>/",
        gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({"patch": "update"}),
        name="patch_gold_cert_price_config",
    ),
    path(
        "<int:id>/",
        gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({"delete": "destroy"}),
        name="delete_gold_cert_price_config",
    ),
    path(
        "<int:id>/",
        gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({"get": "retrieve"}),
        name="get_gold_cert_price_config",
    ),
]

cert_urls = [
    path(
        "",
        cert_view.CertViewSet.as_view({"get": "list"}),
        name="list_cert",
    ),
    path(
        "create",
        cert_view.CertViewSet.as_view({"post": "create"}),
        name="create_cert",
    ),
    path(
        "<int:id>/",
        cert_view.CertViewSet.as_view({"patch": "update"}),
        name="patch_cert",
    ),
    path(
        "<int:id>/",
        cert_view.CertViewSet.as_view({"delete": "destroy"}),
        name="delete_cert",
    ),
    path(
        "<int:id>/",
        cert_view.CertViewSet.as_view({"get": "retrieve"}),
        name="get_cert",
    ),
]

gold_price_urls = [
    path(
        "",
        gold_price_view.GoldPriceServiceViewSet.as_view({"get": "list"}),
        name="list_gold_price",
    ),
    path(
        "create",
        gold_price_view.GoldPriceServiceViewSet.as_view({"post": "create"}),
        name="create_gold_price",
    ),
    path(
        "<str:id>/",
        gold_price_view.GoldPriceServiceViewSet.as_view({"patch": "update"}),
        name="patch_gold_price",
    ),
    path(
        "active",
        gold_price_view.GoldPriceServiceViewSet.as_view({"get": "get_active"}),
        name="get_active_gold_price",
    ),
    path(
        "<str:id>/",
        gold_price_view.GoldPriceServiceViewSet.as_view({"delete": "destroy"}),
        name="delete_gold_price",
    ),
    path(
        "<str:id>/",
        gold_price_view.GoldPriceServiceViewSet.as_view({"get": "retrieve"}),
        name="get_gold_price",
    ),
]


gold_price_config_urls = [
    path(
        "",
        gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({"get": "list"}),
        name="list_gold_config",
    ),
    path(
        "create",
        gold_price_config_view.GoldPriceConfigServiceViewSet.as_view(
            {"post": "create"}
        ),
        name="create_gold_config",
    ),
    path(
        "<str:id>/",
        gold_price_config_view.GoldPriceConfigServiceViewSet.as_view(
            {"patch": "update"}
        ),
        name="patch_gold_config",
    ),
    path(
        "<str:id>/",
        gold_price_config_view.GoldPriceConfigServiceViewSet.as_view(
            {"delete": "destroy"}
        ),
        name="delete_gold_config",
    ),
    path(
        "<str:id>/",
        gold_price_config_view.GoldPriceConfigServiceViewSet.as_view(
            {"get": "retrieve"}
        ),
        name="get_gold_config",
    ),
]

gold_promo_urls = [
    path(
        "",
        gold_promo_view.GoldPromoViewSet.as_view({"get": "list"}),
        name="list_gold_promo",
    ),
    path(
        "create",
        gold_promo_view.GoldPromoViewSet.as_view({"post": "create"}),
        name="create_gold_promo",
    ),
    path(
        "<str:id>/",
        gold_promo_view.GoldPromoViewSet.as_view({"patch": "update"}),
        name="patch_gold_promo",
    ),
    path(
        "<str:id>/",
        gold_promo_view.GoldPromoViewSet.as_view({"delete": "destroy"}),
        name="delete_gold_promo",
    ),
    path(
        "<str:id>/",
        gold_promo_view.GoldPromoViewSet.as_view({"get": "retrieve"}),
        name="get_gold_promo",
    ),
]

urlpatterns = [
    path("", include(gold_urls)),
    path("price/", include(gold_price_urls)),
    path("cert/", include(cert_urls)),
    path("cert_price/", include(gold_cert_price_url)),
    path("price_config/", include(gold_price_config_urls)),
    path("gold_promo/", include(gold_promo_urls)),
]
