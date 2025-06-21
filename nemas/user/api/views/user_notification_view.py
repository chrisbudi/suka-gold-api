from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from user.models.users import user_address
from user.api.serializers import UserAddressSerializer


class user_notification_views(ViewSet):
    """View user prop view in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        tags=["User - User address"],
    )
    def get(self, request):
        # get then
        try:
            user_props = user_address.objects.filter(user=request.user)
            if user_props is None:
                return Response({}, status=404)
            user_props_data = UserAddressSerializer(user_props, many=True)
            return Response(
                user_props_data.data,
                status=200,
            )
        except user_address.DoesNotExist:
            return Response({}, status=404)
