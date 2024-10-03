"""
URL mapping for user app
"""

from django.urls import path
from .views import (
   CreateTokenView, 
   CreateUserView, 
   ManageUserView,
   
   CreateUserKtpView,
   CreateUserPropView,
   RetrieveUpdateUserKtpView,
   RetrieveUpdateUserPropView,
    
)
app_name = "user"

user_view_url =[
]
 


urlpatterns = [
   path('create/', CreateUserView.as_view(), name='create'),
   path('token/', CreateTokenView.as_view(), name='token'),
   path('me/', ManageUserView.as_view(), name='me'),
   
   path('user_prop/create/', CreateUserPropView.as_view(), name='user_prop_create'),
   path('user_prop/', RetrieveUpdateUserPropView.as_view(), name='user_prop_retrieve_update'),
   path('user_ktp/create', CreateUserKtpView.as_view(), name='user_ktp_create'),
   path('user_ktp/', RetrieveUpdateUserKtpView.as_view(), name='user_ktp_retrieve_update'),
   

]
