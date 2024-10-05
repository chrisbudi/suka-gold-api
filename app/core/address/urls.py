"""
Url mapping for the recipe app
"""

from django.urls import path, include

# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    province_view,
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


urlpatterns = [
    path('province/', include(province_url)),
]
