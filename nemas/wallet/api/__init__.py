from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from wallet.api.serializers import (
    TopupVASerializer as modelVASerializer,
    TopupQrisSerializer as modelqrisSerializer,
)
from django.conf import settings


class TopupVaWebhookView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    WEBHOOK_TOKEN = settings.XENDIT.get("WEBHOOK_TOKEN")

    @extend_schema(
        request=modelqrisSerializer,
        responses={200: modelVASerializer},
    )
    def VerifyVaTopup(self, request):
        token = request.headers.get("Authorization")
        if token != f"Bearer {self.WEBHOOK_TOKEN}":
            return JsonResponse({"error": "Unauthorized"}, status=401)
        serializer = modelqrisSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.context.get("response"), status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
