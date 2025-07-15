# urls.py
from django.urls import path
from reporting.api.views import gold_chart_view
from reporting.api.views.gold_transaction_view import GoldTransactionLogView
from reporting.api.views.gold_transaction_avg_view import GoldTransactionAvgView
from reporting.api.views.transaction import user_transaction_view

app_name = "reporting"

user_transaction_view = [
    path(
        "user-transactions/",
        user_transaction_view.user_transaction_view.as_view(),
        name="user_transactions",
    ),
]

urlpatterns = [
    path("gold-transactions/", GoldTransactionLogView.as_view()),
    path("gold-transactions/avg", GoldTransactionAvgView.as_view()),
    path("gold-chart/daily/", gold_chart_view.GoldChartDailyView.as_view()),
    path("gold-chart/weekly/", gold_chart_view.GoldChartWeeklyView.as_view()),
    path("gold-chart/monthly/", gold_chart_view.GoldChartMonthlyView.as_view()),
    # report transaction user
    *user_transaction_view,
]
