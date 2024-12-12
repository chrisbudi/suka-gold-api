from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.api.serializers import UserPinSerializer as modelSerializer


@extend_schema(
    tags=["User - User Pin Create"],
)
class UserPinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the current user's pin
        serializer = modelSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        # Update the current user's pin
        serializer = modelSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
