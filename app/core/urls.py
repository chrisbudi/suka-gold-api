"""
URL mapping for core app
"""

from django.urls import path, include

from core.information.urls import urlpatterns as information_urls

app_name = "core"

urlpatterns = [
   path('information/', include(information_urls)),
]
