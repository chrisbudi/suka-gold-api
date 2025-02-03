"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from rest_framework.authentication import SessionAuthentication

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.authentication import JWTAuthentication
from user.api import urls as userUrl
from core import urls as coreUrl
from wallet.api import urls as walletUrl
from gold_transaction.api import urls as goldUrl

authentication_classes = [JWTAuthentication]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # core shema
    path(
        "api/schema/core/",
        SpectacularAPIView.as_view(urlconf="core.urls"),
        name="core-schema",
    ),
    path(
        "api/schema/core/docs",
        SpectacularSwaggerView.as_view(url_name="core-schema"),
        name="core-swagger-ui",
    ),
    # split schema
    path(
        "api/schema/users/",
        SpectacularAPIView.as_view(urlconf="user.api.urls"),
        name="user-schema",
    ),
    path(
        "api/schema/users/docs",
        SpectacularSwaggerView.as_view(url_name="user-schema"),
        name="user-swagger-ui",
    ),
    # api user
    path("api/users/", include(userUrl), name="user"),
    path("api/core/", include(coreUrl)),
    path("api/wallet/", include(walletUrl)),
    path("api/gold-transaction/", include(goldUrl)),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
