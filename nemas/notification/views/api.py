from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notification.application.dto import NotificationDTO
from notification.application.commands import notify_user
from .serializers import NotificationSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    request=NotificationSerializer,
    responses={
        200: OpenApiResponse(description="Notification sent"),
        400: OpenApiResponse(description="Validation error"),
    },
    tags=["Notifications"],
    summary="Trigger a notification",
    description="Endpoint to trigger a notification to a user.",
)
class TriggerNotificationView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data or {}
            dto = NotificationDTO(
                user_id=validated_data.get("user_id"),
                user_name=validated_data.get("user_name"),
                user_email=validated_data.get("email"),
                title=validated_data.get("title"),
                message=validated_data.get("message"),
                data=validated_data.get("data", {}),
            )
            notify_user(dto)
            return Response({"status": "notification sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
