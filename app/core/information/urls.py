"""
Url mapping for the recipe app
"""
from django.urls import path, include
# from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    informations_customer_service_view as views_customer_service,
    informations_promo_view as views_promo,
    informations_educational_view as views_educational,
    informations_rating_view as views_rating,
    )



router = DefaultRouter()

app_name = 'information'
# customer service
customer_service_urls = [
    path('', views_customer_service.InformationCustomerServiceViewSet.as_view({'get': 'list'}), name='list_customer_service'),
    path('', views_customer_service.InformationCustomerServiceViewSet.as_view({'post': 'create'}), name='post_customer_service'),
    path('<str:id>/', views_customer_service.InformationCustomerServiceViewSet.as_view({'patch': 'update'}), name='patch_customer_service'),
    path('<str:id>/', views_customer_service.InformationCustomerServiceViewSet.as_view({'delete': 'destroy'}), name='delete_customer_service'),
    path('<str:id>/', views_customer_service.InformationCustomerServiceViewSet.as_view({'get': 'retrieve'}), name='get_customer_service'),
]

# educational
educational_urls = [
    path('', views_educational.InformationEducationViewSet.as_view({'get': 'list'}), name='list_educational'),
    path('', views_educational.InformationEducationViewSet.as_view({'post': 'create'}), name='post_educational'),
    path('<int:pk>/', views_educational.InformationEducationViewSet.as_view({'patch': 'update'}), name='patch_educational'),
    path('<int:pk>/', views_educational.InformationEducationViewSet.as_view({'delete': 'destroy'}),  name='delete_educational'),
    path('<int:pk>/', views_educational.InformationEducationViewSet.as_view({'get': 'retrieve'}), name='get_educational'),
]

# promo
promo_urls = [
    path('', views_promo.InformationPromoViewSet.as_view({'get': 'list'}), name='list_promo'),
    path('', views_promo.InformationPromoViewSet.as_view({'post': 'create'}), name='post_promo'),
    path('<str:id>/', views_promo.InformationPromoViewSet.as_view({'patch': 'update'}), name='patch_promo'),
    path('<str:id>/', views_promo.InformationPromoViewSet.as_view({'delete': 'destroy'}), name='delete_promo'),
    path('<str:id>/', views_promo.InformationPromoViewSet.as_view({'get': 'retrieve'}), name='get_promo'),
]

# rating 
rating_urls = [
    path('', views_rating.InformationRatingViewSet.as_view({'get': 'list'}), name='list_rating'),
    path('', views_rating.InformationRatingViewSet.as_view({'post': 'create'}), name='post_rating'),
    path('<str:id>/', views_rating.InformationRatingViewSet.as_view({'patch': 'update'}), name='patch_rating'),
    path('<str:id>/', views_rating.InformationRatingViewSet.as_view({'delete': 'destroy'}), name='delete_rating'),
    path('<str:id>/', views_rating.InformationRatingViewSet.as_view({'get': 'retrieve'}), name='get_rating'),
]

urlpatterns = [
    path('customer_service/', include(customer_service_urls)),
    path('educational/', include(educational_urls)),
    path('promo/', include(promo_urls)),
    path('rating/', include(rating_urls)),
]
