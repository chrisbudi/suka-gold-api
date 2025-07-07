from django.urls import path
from contact.api.views import ContactUsView

urlpatterns = [
    path("api/contact", ContactUsView.as_view(), name="contact-us"),
]

app_name = "contact"
