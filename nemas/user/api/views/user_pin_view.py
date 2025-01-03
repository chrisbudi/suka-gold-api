from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from user.api.serializers import UserPinSerializer as modelSerializer


@extend_schema(
    tags=["User - User Pin Create"],
)
class UserPinView(APIView):
    serializer_class = modelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Return the current user's pin
            serializer = modelSerializer(request.user)
            return Response(serializer.data)
        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        try:
            # Update the current user's pin
            serializer = modelSerializer(request.user, data=request.data, partial=True)
            print(serializer, "serializer")
            if serializer.is_valid():
                print(serializer.validated_data, "serializer data")

                user = serializer.update(request.user, serializer.validated_data)
                print(user, "user")
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
