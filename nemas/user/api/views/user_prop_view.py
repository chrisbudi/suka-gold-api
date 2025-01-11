"""
views for the user API
"""

from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from user.api.serializers import UserPropSerializer
from user.models import user_props as UserProps


@extend_schema(
    tags=["User - User Prop retrieve update"],
)
class UserPropView(APIView):
    """View user prop view in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # get then
        try:
            user_props = UserProps.objects.get(user=request.user)
            user_props_data = dict(UserPropSerializer(user_props).data)
            return Response(
                {
                    "user_id": user_props.user.id,
                    "name": request.user.name,
                    **user_props_data,
                },
                status=200,
            )
        except UserProps.DoesNotExist:
            return Response({}, status=404)
