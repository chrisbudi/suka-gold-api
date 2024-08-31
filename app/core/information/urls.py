"""
Url mapping for the recipe app
"""
from django.urls import path
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

urlpatterns = [
    # customer service
    path('get_customer_service', views_customer_service.fetch_customer_service, name='get_customer_service'),
    path('post_customer_service', views_customer_service.post_customer_service, name='post_customer_service'),
    path('patch_customer_service/<str:id>', views_customer_service.patch_customer_service, name='patch_customer_service'),
    path('delete_customer_service/<str:id>', views_customer_service.delete_customer_service, name='delete_customer_service'),
    # educational
    path('get_educational', views_educational.fetch_educational, name='get_educational'),
    path('post_educational', views_educational.post_educational, name='post_educational'),
    path('patch_educational/<str:id>', views_educational.patch_educational, name='patch_educational'),
    path('delete_educational/<str:id>', views_educational.delete_educational, name='delete_educational'),
    # promo
    path('get_promo', views_promo.fetch_promo, name='get_promo'),
    path('post_promo', views_promo.post_promo, name='post_promo'),
    path('patch_promo/<str:id>', views_promo.patch_promo, name='patch_promo'),
    path('delete_promo/<str:id>', views_promo.delete_promo, name='delete_promo'),
    # rating
    path('get_rating', views_rating.fetch_rating, name='get_rating'),
    path('post_rating', views_rating.post_rating, name='post_rating'),
    path('patch_rating/<str:id>', views_rating.patch_rating, name='patch_rating'),
    path('delete_rating/<str:id>', views_rating.delete_rating, name='delete_rating'),
    
]
