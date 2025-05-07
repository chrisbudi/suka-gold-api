# urls.py
from django.urls import path
from reporting.api.views import gold_chart_view
from reporting.api.views.gold_transaction_view import GoldTransactionLogView

app_name = "reporting"

urlpatterns = [
    path("gold-transactions/", GoldTransactionLogView.as_view()),
    path("gold-chart/daily/", gold_chart_view.GoldChartDailyView.as_view()),
    path("gold-chart/weekly/", gold_chart_view.GoldChartWeeklyView.as_view()),
    path("gold-chart/monthly/", gold_chart_view.GoldChartMonthlyView.as_view()),
]
