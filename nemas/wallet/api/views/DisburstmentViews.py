from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from wallet.api.serializers import (
    DisburstSerializer as modelSerializer,
)


@extend_schema(
    tags=["Disburst - Disburst Transaction Create"],
)
class DisburstTransactionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=modelSerializer,
        responses={201: modelSerializer},
    )
    def generate(self, request):
        serializer = modelSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.context.get("response"), status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
