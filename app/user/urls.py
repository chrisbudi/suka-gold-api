"""
URL mapping for user app
"""
from django.urls import path
from rest_framework.urls import app_name
from user import views

app_name = "user"

url_pattern = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
