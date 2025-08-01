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
from order.api import urls as orderFixUrl
from reporting import urls as reporting_url
from contact import urls as contact_url
from notification import urls as notification_url
from auth_core import urls as auth_core_url
from investment.api import urls as investmentUrl

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
    path("api/users/", include(userUrl, "user"), name="user"),
    path("api/core/", include(coreUrl, "core")),
    path("api/wallet/", include(walletUrl, "wallet")),
    path("api/gold-transaction/", include(goldUrl, "gold-transaction")),
    path(
        "api/schema/order/docs",
        SpectacularSwaggerView.as_view(url_name="order-schema"),
        name="order-swagger-ui",
    ),
    path(
        "api/schema/order/fix",
        SpectacularAPIView.as_view(urlconf="order.api.urls"),
        name="order-fix-schema",
    ),
    path(
        "api/schema/order/fix/docs",
        SpectacularSwaggerView.as_view(url_name="order-fix-schema"),
        name="order-fix-swagger-ui",
    ),
    path("api/orders/fix/", include(orderFixUrl, "order_fix")),
    path("api/reports/", include(reporting_url, "reporting")),
    path("api/contact/", include(contact_url, "contact")),
    path("api/notification/", include(notification_url, "notification")),
    path("api/authentication/", include(auth_core_url, "auth_core")),
    path("api/investment/", include(investmentUrl, "investment")),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
