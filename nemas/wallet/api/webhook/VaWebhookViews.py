from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from wallet.api.serializers.WebhookVASerializer import (
    VirtualAccountPaymentWebhookSerializer,
)


@api_view(["POST"])
def va_webhook_view(request):
    token = request.headers.get("X-Webhook-Token")
    xendit_settings = settings.XENDIT
    if token != xendit_settings.get("WEBHOOK_KEY"):
        return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = VirtualAccountPaymentWebhookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "VA webhook received and saved"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
