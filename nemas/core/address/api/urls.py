"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    province_view,
    city_view,
    district_view,
    sub_district_view,
    postal_code_view,
    customer_pickup_address_view,
)

router = DefaultRouter()

app_name = "address"
# fmt: off


province_url = [
    path('', province_view.ProviceViewSet.as_view({'get': 'list'}), name='list_province'),
    path('create', province_view.ProviceViewSet.as_view({'post': 'create'}), name='post_province'),
    path('<int:id>', province_view.ProviceViewSet.as_view({'patch': 'update'}), name='patch_province'),
    path('<int:id>', province_view.ProviceViewSet.as_view({'delete': 'destroy'}), name='delete_province'),
    path('<int:id>', province_view.ProviceViewSet.as_view({'get': 'retrieve'}), name='get_province')
]

city_url = [
    path('', city_view.CityViewSet.as_view({'get': 'list'}), name='list_city'),
    path('create', city_view.CityViewSet.as_view({'post': 'create'}), name='post_city'),
    path('<int:id>', city_view.CityViewSet.as_view({'patch': 'update'}), name='patch_city'),
    path('<int:id>', city_view.CityViewSet.as_view({'delete': 'destroy'}), name='delete_city'),
    path('<int:id>', city_view.CityViewSet.as_view({'get': 'retrieve'}), name='get_city')
]


district_url = [
    path('', district_view.DistrictViewSet.as_view({'get': 'list'}), name='list_district'),
    path('create', district_view.DistrictViewSet.as_view({'post': 'create'}), name='post_district'),
    path('<int:id>', district_view.DistrictViewSet.as_view({'patch': 'update'}), name='patch_district'),
    path('<int:id>', district_view.DistrictViewSet.as_view({'delete': 'destroy'}), name='delete_district'),
    path('<int:id>', district_view.DistrictViewSet.as_view({'get': 'retrieve'}), name='get_district')
]


subdistrict_url = [
    path('', sub_district_view.SubDistrictViewSet.as_view({'get': 'list'}), name='list_sub_district'),
    path('create', sub_district_view.SubDistrictViewSet.as_view({'post': 'create'}), name='post_sub_district'),
    path('<int:id>', sub_district_view.SubDistrictViewSet.as_view({'patch': 'update'}), name='patch_sub_district'),
    path('<int:id>', sub_district_view.SubDistrictViewSet.as_view({'delete': 'destroy'}), name='delete_sub_district'),
    path('<int:id>', sub_district_view.SubDistrictViewSet.as_view({'get': 'retrieve'}), name='get_sub_district')
]


postal_code_url = [
    path('', postal_code_view.PostalCodeViewSet.as_view({'get': 'list'}), name='list_postal_code'),
    path('create', postal_code_view.PostalCodeViewSet.as_view({'post': 'create'}), name='post_postal_code'),
    path('<int:id>', postal_code_view.PostalCodeViewSet.as_view({'patch': 'update'}), name='patch_postal_code'),
    path('<int:id>', postal_code_view.PostalCodeViewSet.as_view({'delete': 'destroy'}), name='delete_postal_code'),
    path('<int:id>', postal_code_view.PostalCodeViewSet.as_view({'get': 'retrieve'}), name='get_postal_code')
]


customer_pickup_address_url = [
    path('', customer_pickup_address_view.CustomerPickupAddressViewSet.as_view({'get': 'list'}), name='list_customer_pickup_address'),
    path('create', customer_pickup_address_view.CustomerPickupAddressViewSet.as_view({'post': 'create'}), name='post_customer_pickup_address'),
    path('<int:id>', customer_pickup_address_view.CustomerPickupAddressViewSet.as_view({'patch': 'update'}), name='patch_customer_pickup_address'),
    path('<int:id>', customer_pickup_address_view.CustomerPickupAddressViewSet.as_view({'delete': 'destroy'}), name='delete_customer_pickup_address'),
    path('<int:id>', customer_pickup_address_view.CustomerPickupAddressViewSet.as_view({'get': 'retrieve'}), name='get_customer_pickup_address'),
]




urlpatterns = [
    path('province/', include(province_url)),
    path('city/', include(city_url)),
    path('district/', include(district_url)),
    path('sub_district/', include(subdistrict_url)),
    path('postal_code/', include(postal_code_url)),
    path('customer_pickup/', include(customer_pickup_address_url)),
]
