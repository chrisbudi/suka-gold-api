"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    delivery_partner_service_view,
    delivery_partner_view,
)

router = DefaultRouter()

app_name = "delivery"
# fmt: off


delivery_partner_url = [
    path('', delivery_partner_view.DeliveryPartnerViewSet.as_view({'get': 'list'}), name='list_delivery_partner'),
    path('create', delivery_partner_view.DeliveryPartnerViewSet.as_view({'post': 'create'}), name='post_delivery_partner'),
    path('<int:id>', delivery_partner_view.DeliveryPartnerViewSet.as_view({'patch': 'update'}), name='patch_delivery_partner'),
    path('<int:id>', delivery_partner_view.DeliveryPartnerViewSet.as_view({'delete': 'destroy'}), name='delete_delivery_partner'),
    path('<int:id>', delivery_partner_view.DeliveryPartnerViewSet.as_view({'get': 'retrieve'}), name='get_delivery_partner')
]

delivery_partner_service_url = [
    path('', delivery_partner_service_view.DeliveryPartnerServiceViewSet.as_view({'get': 'list'}), name='list_delivery_partner_service'),
    path('create', delivery_partner_service_view.DeliveryPartnerServiceViewSet.as_view({'post': 'create'}), name='post_delivery_partner_service'),
    path('<int:id>', delivery_partner_service_view.DeliveryPartnerServiceViewSet.as_view({'patch': 'update'}), name='patch_delivery_partner_service'),
    path('<int:id>', delivery_partner_service_view.DeliveryPartnerServiceViewSet.as_view({'delete': 'destroy'}), name='delete_delivery_partner_service'),
    path('<int:id>', delivery_partner_service_view.DeliveryPartnerServiceViewSet.as_view({'get': 'retrieve'}), name='get_delivery_partner_service'),
]




urlpatterns = [
    path('', include(delivery_partner_url)),
    path('service/', include(delivery_partner_service_url)),
]
