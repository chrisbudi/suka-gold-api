"""
views for the user API
"""

from rest_framework import permissions
from rest_framework.settings import api_settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from shared.utils.notification import create_user_notification
from user.api.serializers import UserPropSerializer, UserPropBankSerializer
from user.models import user_props as UserProps


class UserPropView(ViewSet):
    """View user prop view in the system"""

    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        tags=["User - User Prop retrieve update"],
    )
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

    @extend_schema(
        tags=["User - User prop - update bank"],
        request=UserPropBankSerializer,
    )
    def bank_submit(self, request):
        serialize = UserPropBankSerializer(data=request.data)
        if serialize.is_valid():
            user_props = UserProps.objects.get(user=request.user)
            user_props.bank_account_code = serialize.data["bank_account_code"]
            user_props.bank_account_number = serialize.data["bank_account_number"]
            user_props.bank_account_holder_name = serialize.data[
                "bank_account_holder_name"
            ]
            user_props.save()
            return Response(serialize.data, status=200)

        return Response(serialize.errors, status=400)
