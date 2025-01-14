from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from user.api.serializers import (
    UserPinSerializer as modelSerializer,
    UserPinVerifySerializer as modelVerifySerializer,
)


@extend_schema(
    tags=["User - User Pin Create"],
)
class UserPinView(viewsets.ModelViewSet):
    serializer_class = modelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # get user pin
            serializer = modelSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        try:
            # Update the current user's pin
            serializer = modelSerializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def verify(self, request):
        try:
            # validate pin of the current user
            serializer = modelVerifySerializer(request.user, data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
