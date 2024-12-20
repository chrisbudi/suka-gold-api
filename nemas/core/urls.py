"""
URL mapping for core app
"""

from django.urls import path, include

from core.gold.urls import urlpatterns as gold_urls
from core.information.api.urls import urlpatterns as information_urls
from core.address.api.urls import urlpatterns as address_urls
from core.payment.urls import urlpatterns as payment_urls
from . import consumer

app_name = "core"

urlpatterns = [
    path("gold/", include(gold_urls)),
    path("information/", include(information_urls)),
    path("address/", include(address_urls)),
    path("payment/", include(payment_urls)),
]

websocket_urlpatterns = [
    path("ws/gold/", consumer.PriceConsumer.as_asgi()),
]
