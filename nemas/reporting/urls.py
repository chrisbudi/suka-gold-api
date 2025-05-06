# urls.py
from django.urls import path
from reporting.api.views import GoldTransactionLogView

app_name = "reporting"

urlpatterns = [
    path("gold-transactions/", GoldTransactionLogView.as_view()),
]
