"""
URL mapping for core app
"""

from django.urls import path, include

from core.gold.urls import urlpatterns as gold_urls
from core.information.api.urls import urlpatterns as information_urls
from core.address.api.urls import urlpatterns as address_urls
from core.payment.urls import urlpatterns as payment_urls
from core.delivery.api.urls import urlpatterns as delivery_partner_urls
from core.admin.api.urls import urlpatterns as admin_fee_urls
from core.investment.api.urls import urlpatterns as investment_return_urls

app_name = "core"

urlpatterns = [
    path("gold/", include(gold_urls)),
    path("information/", include(information_urls)),
    path("address/", include(address_urls)),
    path("payment/", include(payment_urls)),
    path("delivery_partner/", include(delivery_partner_urls)),
    path("admin_fee/", include(admin_fee_urls)),
    path("investment_return/", include(investment_return_urls)),
]
