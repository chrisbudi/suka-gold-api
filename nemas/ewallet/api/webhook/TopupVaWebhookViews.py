import json
import logging
from venv import logger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from ewallet.models import topup_qris_webhook
from ewallet.api.serializers.WebhookTopupQrisSerializer import (
    TopupWebhookSerializer,
)
from django.views import View
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from django.conf import settings

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class TopupVaWebhookView(viewsets.ModelViewSet):
    @extend_schema(
        request=TopupWebhookSerializer,
        responses={200: None, 400: None, 401: None, 500: None},
        tags=["Topup QRIS Webhook"],
        description="Endpoint to handle QRIS topup webhooks",
    )
    def post(self, request, *args, **kwargs):
        WEBHOOK_TOKEN = settings.XENDIT.get("WEBHOOK_KEY")
        api_key = request.headers.get("x-callback-token")
        print(api_key, WEBHOOK_TOKEN, "print webhook")
        if api_key != WEBHOOK_TOKEN:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        # Validate payload
        serializer = TopupWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                {"error": "Invalid payload", "details": serializer.errors}, status=400
            )

        payload = serializer.validated_data
        payment_data = payload["data"]

        try:
            # Check for duplicate
            if topup_qris_webhook.objects.filter(
                payment_id=payment_data["id"]
            ).exists():
                return JsonResponse({"status": "already_processed"}, status=200)

            # Create payment record
            payment_record = topup_qris_webhook.objects.create(
                event_type=payload["event"],
                payment_id=payment_data["id"],
                business_id=payload["business_id"],
                currency=payment_data["currency"],
                amount=payment_data["amount"],
                status=payment_data["status"],
                qr_id=payment_data["qr_id"],
                reference_id=payment_data.get("reference_id", ""),
                channel_code=payment_data["channel_code"],
                expires_at=payment_data["expires_at"],
                metadata=payment_data.get("metadata", {}),
                payment_detail=payment_data.get("payment_detail", {}),
                raw_data=request.data,
            )

            # Process topup only for succeeded payments
            if payment_data["status"] == "SUCCEEDED":
                # Add your topup processing logic here
                # Example:
                # user = get_user_from_reference(payment_data['reference_id'])
                # user.balance += payment_data['amount']
                # user.save()
                logger.info(f"Processed topup for {payment_data['amount']} IDR")

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            logger.error(f"Webhook processing failed: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)
