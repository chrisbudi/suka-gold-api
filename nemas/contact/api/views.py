import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contact.api.serializers import ContactRequestSerializer
from contact.application.commands.submit_contact_request import (
    SubmitContactRequestCommand,
    SubmitContactRequestHandler,
)
from contact.application.commands.list_contact_queries import (
    ListContactRequestsQuery,
    ListContactRequestsHandler,
)
from contact.application.services.contact_service import ContactService
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import pagination
from contact.infrastucture.repositories.django_contact_repository import (
    DjangoContactRequestRepository,
)


class ContactUsView(APIView):

    @extend_schema(
        request=ContactRequestSerializer,
    )
    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                command = SubmitContactRequestCommand(
                    first_name=serializer.validated_data.get("first_name"),
                    last_name=serializer.validated_data.get("last_name"),
                    email=serializer.validated_data.get("email"),
                    phone=serializer.validated_data.get("phone"),
                    message=serializer.validated_data.get("message"),
                )
                repo = DjangoContactRequestRepository()
                service = ContactService(repo)
                print("Submitting contact request with command:", command)
                handler = SubmitContactRequestHandler(service)
                print("Handling command with handler:", handler)
                handler.handle(command)
                print("Contact request submitted successfully")
                return Response(
                    {"message": "Contact request submitted"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error("Error submitting contact request", exc_info=True)
            # Return clear JSON error response with exception info (avoid exposing sensitive debug info in production)
            return Response(
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    # "traceback": traceback.format_exc()  # Optional: include for dev only
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        methods=["GET"],
        summary="List contact requests",
        parameters=[
            OpenApiParameter(
                name="limit", type=int, location=OpenApiParameter.QUERY, required=False
            ),
            OpenApiParameter(
                name="offset", type=int, location=OpenApiParameter.QUERY, required=False
            ),
        ],
        responses=ContactRequestSerializer(many=True),
    )
    def get(self, request):
        repo = DjangoContactRequestRepository()
        handler = ListContactRequestsHandler(repo)
        query = ListContactRequestsQuery()
        contact_requests = handler.handle(query)
        paginator = pagination.LimitOffsetPagination()
        page = paginator.paginate_queryset(contact_requests, request, view=self)
        serializer = ContactRequestSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
