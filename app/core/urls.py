"""
URL mapping for core app
"""

from django.urls import path, include

from core.gold.urls import urlpatterns as gold_urls
from core.information.urls import urlpatterns as information_urls

app_name = "core"

urlpatterns = [
   path('gold/', include(gold_urls)),
   path('information/', include(information_urls)),
]
