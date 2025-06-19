from django.urls import path
from notification.views import api


app_name = "notification"

urlpatterns = [
    path("notify/", api.TriggerNotificationView.as_view(), name="notify"),
]
