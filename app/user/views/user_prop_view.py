"""
views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.serializers import (
    UserPropSerializer,
    UserKtpSerializer
)

@extend_schema(
    tags=['User - User Prop create'],
)
class CreateUserPropView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserPropSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)


@extend_schema(
    tags=['User - User Prop retrieve update'],
)
class RetrieveUpdateUserPropView(generics.RetrieveUpdateAPIView):
    """Create a new user in the system"""
    serializer_class = UserPropSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


@extend_schema(
    tags=['User - User ktp create'],
)
class CreateUserKtpView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserKtpSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)
    

@extend_schema(
    tags=['User - User ktp retrieve update'],
)
class RetrieveUpdateUserKtpView(generics.RetrieveUpdateAPIView):
    """Create a new user in the system"""
    serializer_class = UserKtpSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

