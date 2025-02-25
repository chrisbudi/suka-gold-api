"""
views for the user API
"""

from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from user.models.users import user_address
from user.api.serializers import UserAddressSerializer


class UserAddressView(ViewSet):
    """View user prop view in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        tags=["User - User address"],
    )
    def get(self, request):
        # get then
        try:
            user_props = user_address.objects.get(user=request.user)
            if user_props is None:
                return Response({}, status=404)
            user_props_data = dict(UserAddressSerializer(user_props).data)
            return Response(
                {
                    "user_id": user_props.user.id,
                    **user_props_data,
                },
                status=200,
            )
        except user_address.DoesNotExist:
            return Response({}, status=404)

    @extend_schema(
        tags=["User - User address"],
        request=UserAddressSerializer,
    )
    def address_submit(self, request):
        serialize = UserAddressSerializer(data=request.data)
        if serialize.is_valid():
            address, _ = user_address.objects.get_or_create(user=request.user)
            print(address, "address")
            if address is None:
                address = user_address()
                address.user = request.user
            address.address = serialize.data["address"]
            address.city = serialize.data["city"]
            address.district = serialize.data["district"]
            address.subdistrict = serialize.data["subdistrict"]
            address.postal_code = serialize.data["postal_code"]
            address.save()
            return Response(serialize.data, status=200)
        return Response(serialize.errors, status=400)
