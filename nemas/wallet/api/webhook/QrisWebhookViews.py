from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app import settings
from wallet.api.serializers.WebhookQrisSerializer import (
    QRISPaymentWebhookSerializer,
)


@api_view(["POST"])
def qris_webhook_view(request):
    # Get token from header
    # token = request.headers.get("X-CALLBACK-TOKEN")

    # # Validate token
    # xendit_settings = settings.XENDIT
    # if token != xendit_settings.get("WEBHOOK_KEY"):
    #     return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    # Deserialize and save
    serializer = QRISPaymentWebhookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "QRIS webhook received and saved"},
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
