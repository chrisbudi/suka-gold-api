"""
Url mapping for the recipe app
"""
from django.urls import path, include
# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    gold_view,
    gold_price_config_view,
    gold_cert_price_view
    )

router = DefaultRouter()

app_name = 'gold'
# customer service
gold_urls = [
    path('', gold_view.GoldServiceViewSet.as_view({'get': 'list'}), name='list_gold'),
    path('create', gold_view.GoldServiceViewSet.as_view({'post': 'create'}), name='post_gold'),
    path('<str:id>/', gold_view.GoldServiceViewSet.as_view({'patch': 'update'}), name='patch_gold'),
    path('<str:id>/', gold_view.GoldServiceViewSet.as_view({'delete': 'destroy'}), name='delete_gold'),
    path('<str:id>/', gold_view.GoldServiceViewSet.as_view({'get': 'retrieve'}), name='get_gold'),
]

gold_cert_price_urls = [
    path('', gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({'get': 'list'}), name='list_gold_cert_price_config'),
    path('create', gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({'post': 'create'}), name='create_gold_cert_price_config'),
    path('<int:id>/', gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({'patch': 'update'}), name='patch_gold_cert_price_config'),
    path('<int:id>/', gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({'delete': 'destroy'}), name='delete_gold_cert_price_config'),
    path('<int:id>/', gold_cert_price_view.GoldCertPriceServiceViewSet.as_view({'get': 'retrieve'}), name='get_gold_cert_price_config'),
]

gold_price_config_urls = [
    path('', gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({'get': 'list'}), name='list_gold_config'),
    path('create', gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({'post': 'create'}), name='create_gold_config'),
    path('<int:id>/', gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({'patch': 'update'}), name='patch_gold_config'),
    path('<int:id>/', gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({'delete': 'destroy'}), name='delete_gold_config'),
    path('<int:id>/', gold_price_config_view.GoldPriceConfigServiceViewSet.as_view({'get': 'retrieve'}), name='get_gold_config'),
]

urlpatterns = [
    path('', include(gold_urls)),
    path('cert_price/', include(gold_cert_price_urls)),
    path('price_config/', include(gold_price_config_urls)),
]
