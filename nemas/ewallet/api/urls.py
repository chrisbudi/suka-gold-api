"""
URL mapping for ewallet app
"""

from django.urls import path
from .views import TopupTransactionView

app_name = "ewallet"

ewallet_view_url = [
    path("topup/", TopupTransactionView.as_view({"post": "generate_va"}), name="topup"),
]


urlpatterns = []
